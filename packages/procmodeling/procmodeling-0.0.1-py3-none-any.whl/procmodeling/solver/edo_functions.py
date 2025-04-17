import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from .utils import *


class edo_functions:

    def __init__(self, name:str, verbose:bool=True):

        self.verbose = verbose

        self.diff_equations = {}
        self.expressions = {}
        self.params = {}
        self.lines = []

        filepath = Path(name)
        if filepath.is_file():
            self._read_txt(name)
            print('edo_functions: Document was read')
        else:
            self._read_docstr(name)
            print('edo_functions: Docstring was read')


    def _read_txt(self, filename:str):
        with open(filename, 'r', encoding="utf-8") as file:
            self.lines = file.readlines()
        self._read_expressions()

    def _read_docstr(self, docstr:str):
        self.lines = docstr.split('\n')
        self._read_expressions()


    def _read_expressions(self):
        diff_equations = {}
        expressions = {}
        params = {}
        for line in self.lines:
            # Remove spaces at the beginning and at the end of the string
            line = line.strip()

            if not(line.startswith('#')):
                # Read ODE. Format: dydt = f(y, t, params)
                if line.startswith('dydt'):
                    pattern = re.search(r'dydt\[(\d+)\]', line) # the "dydt[i]" pattern
                    if pattern:
                        diff_equations[int(line[5])] = line.split('=')[1].strip()
                # Read other expressions
                elif ('=' in line):
                    key, value = line.split('=')
                    if _is_number(value):
                        params[key.strip()] = float(value.strip())
                    else:
                        expressions[key.strip()] = value.strip()

        self.diff_equations = diff_equations
        self.expressions = expressions
        self.params = params

        if self.verbose:
            self.show_equations()




    def show_equations(self):
        laxtext = ' '
        if self.diff_equations:
            # Add the diff_equations in laxtext
            left_text = [f'dy_{i}/dt' for i in self.diff_equations.keys()]
            laxtext += _expressionlist_2_latex(left_text, self.diff_equations.values(), begin='\Longrightarrow')
            
            # highlight in bold the keys of "self.expressions"
            for var in self.expressions.keys():
                # The character "_i" will be replaced by "{i}". i.e. "A_i" to "A{i}"
                var2 = re.sub(r'_(\w+)', r'_{\1}', var)
                var2 = re.sub(r'(?<=[a-zA-Z])(\d+)(?![a-zA-Z])', r'_{\1}', var2)
                check_if_exists = _find_and_replace_expression(re.escape(var2), rf'\\mathbf{{{var2}}}', laxtext)
                laxtext = check_if_exists if check_if_exists else laxtext

            # Add the expressions in laxtext
            if self.expressions:
                laxtext += '\n '
                laxtext += _expressionlist_2_latex(self.expressions.keys(), self.expressions.values(), begin='\Rightarrow')
            # Add the paramns in laxtext
            if self.params:
                laxtext += '\n $\it{Parameters:}$\n '
                right_text = list(map(str, self.params.values()))
                laxtext += _expressionlist_2_latex(self.params.keys(), right_text, begin=r'\rightarrow')
        else:
            print('No equations found')

        _plot_text(laxtext)




    def _create_function(self):
        
        # Replace the right side variables in "self.expressions" that are not parameters.
        check = [True]
        repl_expression = self.expressions.copy()
        while any(check):
            check=[]
            for var1 in self.expressions.keys():
                for var2 in self.expressions.keys():
                    if not ( var1 == var2 ):
                        var_in_expr = _find_and_replace_expression(
                            var2, 
                            r'(' + self.expressions[var2] + r')', 
                            repl_expression[var1]
                            )
                        if var_in_expr:
                            check+=[True]
                            repl_expression[var1] = var_in_expr
                        else:
                            check+=[False]
        # Replace the right side variables in "self.diff_equations" that are not parameters.
        repl_equations = self.diff_equations.copy()
        for i in repl_equations.keys():
            for var, expr in repl_expression.items():
                check_if_exists = _find_and_replace_expression(var, r'(' + expr + r')', repl_equations[i])
                repl_equations[i] = check_if_exists if check_if_exists else repl_equations[i]
        
        #####################################################
        # display(list(repl_equations.values()), self.params)
        #####################################################

        # Def function that will create the solve_ivp default function using
        # the "repl_equations" strings and "self.params" dict
        def call_function(equations:list, params):
            # Declare predefined functions
            
            
            predefine_func = {
                'sqrt':np.sqrt,
                'exp':np.exp
            }

            def ode_system(t, y):
                
                dydt = []
                for eq in equations:
                    dydt.append(eval(eq, {**params, 'y': y, 't': t, **predefine_func}))
                return dydt
            return ode_system
        
        self.function = call_function(repl_equations.values(), self.params)




    def solve(self,
            t_span:list, 
            y0:list, 
            t_eval= None,
            method:str = 'RK45',
            show_plot = True,
            ):
        
        self._create_function()

        n_points = 100
        if not(t_eval):
            t_eval = np.linspace(t_span[0], t_span[1], n_points)

        self.result = solve_ivp(self.function, 
                                t_span,
                                y0,
                                method = method,
                                t_eval = t_eval,
                                )
        
        if show_plot == True:
            self._plot_results()



    def _plot_results(self):
        var_count = len(self.result.y)
        fig, axs = plt.subplots(1, var_count, figsize=[2.5*var_count, 2.5])
        
        for i in range(var_count):
            axs[i].plot(self.result.t, self.result.y[i], color='black')
            axs[i].set_title(f'Variable {i}')
            axs[i].set_xlabel('time')
            axs[i].set_ylabel(f'Variable {i}')
        
        fig.tight_layout()