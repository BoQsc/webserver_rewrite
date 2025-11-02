
import os
import sys
import ast
from collections import defaultdict

# --- Configuration ---
ROOT_PROJECT_PATH = os.path.abspath(os.getcwd())
# The minimum threshold for a function to be considered highly coupled/complex.
COUPLING_THRESHOLD = 5

class CallGraphAnalyzer(ast.NodeVisitor):
    """
    A custom AST visitor to collect function definitions and function calls
    within a single Python file, building a local call graph.
    """
    def __init__(self, filepath):
        self.filepath = os.path.relpath(filepath, ROOT_PROJECT_PATH)
        self.defined_functions = set()
        self.function_calls = defaultdict(set)
        self.current_function = None

    def _get_function_key(self, func_name):
        """Creates a unique key (filepath::function_name) for a function."""
        return f"{self.filepath}::{func_name}"

    def visit_FunctionDef(self, node):
        """Called when a 'def function_name(...):' is encountered."""
        func_key = self._get_function_key(node.name)
        self.defined_functions.add(func_key)

        # Set the context for subsequent Call nodes within this function's body
        self.current_function = func_key
        # Continue traversing the body of the function
        self.generic_visit(node)
        self.current_function = None

    def visit_AsyncFunctionDef(self, node):
        """Handle async def functions as well."""
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        """Called when a function call (e.g., 'foo(x)') is encountered."""
        if self.current_function:
            # Try to extract the name of the function being called
            called_name = None
            if isinstance(node.func, ast.Name):
                # Simple call: function_name()
                called_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                # Method call or module call: obj.method() or module.function()
                called_name = node.func.attr

            if called_name:
                # We only record the name, we don't know the full module path yet.
                self.function_calls[self.current_function].add(called_name)

        # Continue traversing arguments and keywords
        self.generic_visit(node)


def analyze_project(root_dir):
    """
    Scans the project structure, analyzes all Python files, and aggregates
    the call graph and dependency metrics.
    """
    global ROOT_PROJECT_PATH
    ROOT_PROJECT_PATH = os.path.abspath(root_dir)

    all_defined_functions = set()
    raw_call_graph = defaultdict(set) # {caller_key: {called_names}}

    print(f"--- Scanning project: {ROOT_PROJECT_PATH} ---")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out virtual environments and standard hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(('.', '__')) and d not in ('venv', 'env', 'node_modules')]

        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                print(f"  Parsing: {os.path.relpath(filepath, root_dir)}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        tree = ast.parse(file.read())
                except Exception as e:
                    print(f"    WARNING: Could not parse {filepath}: {e}")
                    continue

                analyzer = CallGraphAnalyzer(filepath)
                analyzer.visit(tree)

                # Aggregate data from the single file analysis
                all_defined_functions.update(analyzer.defined_functions)
                raw_call_graph.update(analyzer.function_calls)

    # --- Phase 2: Build Final Call Graph and Metrics ---

    # Normalize calls: Map raw called names to the full function keys
    final_call_graph = defaultdict(set) # {caller_key: {called_keys}}
    indegree = defaultdict(int)        # {function_key: number_of_callers}
    outdegree = defaultdict(int)       # {function_key: number_of_functions_called}

    local_function_names = {key.split('::')[-1] for key in all_defined_functions}

    for caller_key, called_names in raw_call_graph.items():
        out_count = 0
        for called_name in called_names:
            # Check if the called name is one of our locally defined functions
            if called_name in local_function_names:
                # Simple resolution: we assume the function is defined either in the same file
                # or we just match by name (this is a simplified approach, a real tool
                # would need import resolution).
                
                # Best effort: find all functions with that simple name
                possible_callees = [f for f in all_defined_functions if f.endswith(f"::{called_name}")]
                
                for callee_key in possible_callees:
                    final_call_graph[caller_key].add(callee_key)
                    indegree[callee_key] += 1
                    out_count += 1
        
        # Calculate outdegree based on resolved *internal* dependencies
        outdegree[caller_key] = out_count

    # Initialize indegree for functions that are never called internally
    for func_key in all_defined_functions:
        if func_key not in indegree:
            indegree[func_key] = 0

    return all_defined_functions, indegree, outdegree


def generate_report(defined_functions, indegree, outdegree):
    """Generates a structured text report based on the calculated metrics."""

    print("\n" + "="*80)
    print("                 PROJECT RESTRUCTURING ANALYSIS REPORT")
    print("="*80)

    # 1. High Indegree Functions (Centralized Logic/High Reusability)
    high_indegree = sorted(
        [(count, func) for func, count in indegree.items() if count >= COUPLING_THRESHOLD],
        key=lambda x: x[0], reverse=True
    )
    print("\n--- 1. HIGH INDEGREE FUNCTIONS (High Coupling/Reusability) ---")
    print("  These functions are called by many other parts of the codebase.")
    print("  Consider: Are they well-tested? Could they be broken into smaller utilities?")
    
    if high_indegree:
        for count, func in high_indegree:
            print(f"  [{count:2} calls]: {func}")
    else:
        print(f"  (No functions found with {COUPLING_THRESHOLD}+ internal callers.)")

    # 2. High Outdegree Functions (High Complexity/Low Cohesion)
    high_outdegree = sorted(
        [(count, func) for func, count in outdegree.items() if count >= COUPLING_THRESHOLD],
        key=lambda x: x[0], reverse=True
    )
    print("\n--- 2. HIGH OUTDEGREE FUNCTIONS (High Complexity/Low Cohesion) ---")
    print("  These functions call many other internal functions. Potential 'God Functions'.")
    print("  Consider: Do they handle too many responsibilities? Can they be split?")

    if high_outdegree:
        for count, func in high_outdegree:
            print(f"  [{count:2} calls]: {func}")
    else:
        print(f"  (No functions found that call {COUPLING_THRESHOLD}+ internal functions.)")


    # 3. Uncalled Functions (Dead Code Candidates)
    dead_code = sorted([func for func, count in indegree.items() if count == 0])
    
    # Filter out common entry points like 'main' which naturally have 0 internal callers
    entry_points_to_ignore = {'main', '__init__'}
    true_dead_code = [
        func for func in dead_code 
        if func.split('::')[-1] not in entry_points_to_ignore 
        and not func.split('::')[-1].startswith('_') # Ignore private helper functions 
    ]

    print("\n--- 3. UNCALLED FUNCTIONS (Dead Code Candidates) ---")
    print("  These functions are defined but not called by any other functions in the project.")
    print("  Consider: Are they external API entry points, or simply unused code?")
    
    if true_dead_code:
        for func in true_dead_code:
            print(f"  [0 calls]: {func}")
    else:
        print("  (No clear dead code candidates found.)")

    # 4. Summary
    total_functions = len(defined_functions)
    total_calls_recorded = sum(indegree.values())

    print("\n" + "-"*80)
    print(f"SUMMARY:")
    print(f"  Total Python files scanned: {len(defined_functions) // 2 or 'Multiple'}") # Crude estimate
    print(f"  Total functions defined: {total_functions}")
    print(f"  Total internal calls recorded: {total_calls_recorded}")
    print(f"  High Coupling Threshold: {COUPLING_THRESHOLD}")
    print("-" * 80)
    print("\nNote: This tool is simplified and does not fully resolve imports or method calls.")
    print("It provides function-level dependency hints for restructuring.")


if __name__ == "__main__":
    # Determine the root directory to start from
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = os.getcwd()

    if not os.path.isdir(start_path):
        print(f"Error: The directory '{start_path}' does not exist or is not a directory.")
        sys.exit(1)

    defined, indegree, outdegree = analyze_project(start_path)
    generate_report(defined, indegree, outdegree)
