from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader
from time import process_time
from vending_machine import VendingMachine
from dfa_vending_machine import vm_dfa
import pandas as pd


'(a|b)*a(a|b)(a|b)+'
# ((0|1)*)·(0000|0001|0010|0011|0100|0101|0110|0111|1000|1001|1010|1011|1110)
# ((0|1)*)·(00(00|01|10|11)|01(00|01|10|11)|10(00|01|10|11)|1110)

# ((0|1)*)

program_title = '''

#        AUTÓMATA FINITO        #

¡Genera AFN o AFD a partir de una expresión regular y compara tiempos simulando una cadena! NOTA: para la expresión epsilon, por favor usa la letra "e"
'''

main_menu = '''
¿Qué te gustaría hacer?
1. Probar Maquina Expendedora
2. Establecer una expresión regular
3. Probar una cadena con la expresión regular dada
0. Salir del programa
'''

submenu = '''
Selecciona una de las opciones anteriores para probar tu expresión regular:

    1. Usar Thompson para generar un NFA y construcción de subconjuntos para generar un DFA.
    2. Usar el método directo de DFA.
    0. Volver al menú principal.
'''

thompson_msg = '''
    # THOMPSON Y CONSTRUCCIÓN DE SUBCONJUNTOS # '''

direct_dfa_msg = '''
    # CONSTRUCCIÓN DIRECTA DE AFD # '''

invalid_opt = '''
Error: ¡Esa no es una opción válida!
'''

generate_diagram_msg = '''
¿Te gustaría generar y ver el diagrama? [y/n] (predeterminado: n)'''

type_regex_msg = '''
Escribe una expresión regular '''

type_string_msg = '''
Escribe una cadena '''


if __name__ == "__main__":
    print(program_title)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            # Mostrar ventana vending machine
            vm = VendingMachine()
            vm.show_window()

            # Mostrar tabla de transiciones y diagrama
            transitions = vm_dfa.get_transitions()

            # Convertir las transiciones en una lista de listas (filas)
            transition_list = [(from_state, symbol, to_state) for from_state, symbol, to_state in transitions]

            # Crear un DataFrame con pandas
            df = pd.DataFrame(transition_list, columns=['From State', 'Symbol', 'To State'])

            # Mostrar la tabla
            print(df)

            graph = vm_dfa.trim().to_graphviz()
            graph.attr(rankdir='LR')

            graph.render('./output/DFA.gv', format='pdf', view=True)

        if opt == '2':
            print(type_regex_msg)
            regex = input('> ')

            try:
                reader = Reader(regex)
                tokens = reader.CreateTokens()
                parser = Parser(tokens)
                tree = parser.Parse()

                direct_reader = DirectReader(regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()
                print('\n\tExpression accepted!')
                print('\tParsed tree:', tree)

            except AttributeError as e:
                print(f'\n\tERR: Invalid expression (missing parenthesis)')

            except Exception as e:
                print(f'\n\tERR: {e}')

        if opt == '3':
            if not regex:
                print('\n\tERR: You need to set a regular expression first!')
                opt = None
            else:
                print(submenu)
                method = input('> ')

                if method == '1':
                    print(thompson_msg)
                    print(type_string_msg)
                    regex_input = input('> ')

                    nfa = NFA(tree, reader.GetSymbols(), regex_input)
                    start_time = process_time()
                    nfa_regex = nfa.EvalRegex()
                    stop_time = process_time()

                    print('\nTime to evaluate: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('Does the string belongs to the regex (NFA)?')
                    print('>', nfa_regex)

                    dfa = DFA(nfa.trans_func, nfa.symbols,
                              nfa.curr_state, nfa.accepting_states, regex_input)
                    dfa.TransformNFAToDFA()
                    start_time = process_time()
                    dfa_regex = dfa.EvalRegex()
                    stop_time = process_time()
                    print('\nTime to evaluate: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('Does the string belongs to the regex (DFA)?')
                    print('>', dfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        nfa.WriteNFADiagram()
                        dfa.GraphDFA()

                elif method == '2':
                    print(direct_dfa_msg)
                    print(type_string_msg)
                    regex_input = input('> ')
                    ddfa = DDFA(
                        direct_tree, direct_reader.GetSymbols(), regex_input)
                    start_time = process_time()
                    ddfa_regex = ddfa.EvalRegex()
                    stop_time = process_time()
                    print('\nTime to evaluate: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('Does the string belongs to the regex?')
                    print('>', ddfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        ddfa.GraphDFA()

                    ddfa = None

                elif method == '3':
                    continue

                else:
                    print(invalid_opt)

        elif opt == '0':
            print('See you later!')
            exit(1)