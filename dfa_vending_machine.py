from pythomata import SimpleDFA


# Definición del DFA

alphabet = {"0", "1", "1011","0101","0110","0111","1110","1011","0100","0010","1010","0000","0001","0011","1000", ""}  # 0 y 1 representan monedas y representan la entrada del código del producto. " " representa el string vacio
states = {"q0", "q500", "q1000", "q1500", "q2000", "q2500", "q3000", "q3500", "q4000", "q4500", "q5000", "q5500", "q6000", "q6500", "q1011","q0101","q0110","q0111","q1110","q1011","q0100","q0010","q1010","q0000","q0001","q0011","qmil"}
initial_state = "q0"  # El estado inicial es cuando no se ha ingresado ninguna moneda
accepting_states = {"q2000", "q3000", "q3500", "q4000", "q5000", "q6000","q1011","q0101","q0110","q0111","q1110","q1011","q0100","q0010","q1010","q0000","q0001","q0011","qmil"}  # Los estados donde se alcanzan los precios de productos
transition_function = {
    "q0": {
        "0": "q500",
        "1": "q1000"
        },
        "q500": {
            "0": "q1000",
            "1": "q1500"
        },
        "q1000": {
            "0": "q1500",
            "1": "q2000"
        },
        "q1500": {
            "0": "q2000",
            "1": "q2500"
        },
        "q2000": {
            "0": "q2500",
            "1": "q3500",
            "1011": "q1011"  # Estado de aceptación: se permite ingresar el código del producto con precio 2000
        },
        "q2500": {
            "0": "q3000",
            "1": "q3500"
        },
        "q3000": {
            "0": "q3500",
            "1": "q4000",
            "0101": "q0101",  # Estado de aceptación: se permite ingresar el código del producto con precio 3000
            "0110": "q0110",
            "0111": "q0111"
        },
        "q3500": {
            "0": "q4000",
            "1": "q4500",
            "1110": "q1110",  # Estado de aceptación: se permite ingresar el código del producto con precio 3500
            "1011": "q1011",
            "1000": "qmil",
            "0100": "q0100",
            "0010": "q0010"
        },
        "q4000": {
            "0": "q3500",
            "1": "q4000",
            "1010": "q1010"  # Estado de aceptación: se permite ingresar el código del producto con precio 4000
        },
        "q4500": {
            "0": "q5000",
            "1": "q6000"
        },
        "q5000": {
            "0": "q5500",
            "1": "q6000",
            "0000": "q0000",  # Estado de aceptación: se permite ingresar el código del producto con precio 6000
            "0001": "q0001"
        },
        "q5500": {
            "0": "q5500",
            "1": "q6500"
        },
        "q6000": {
            "0": "q6500",
            "0011": "q0011"  # Estado de aceptación: se permite ingresar el código del producto con precio 6000
        },
        "q6500": {
            "": "q0"
        }, # Estados de aceptación de los productos
        "q1011": {
            "": "q0"
        },
        "q0101": {
            "": "q0"
        },
        "q0110":{
            "": "q0"
        },
        "q0111":{
            "": "q0"
        },
        "q1110":{
            "": "q0"
        },
        "q1011":{
            "": "q0"
        },
        "qmil":{
            "": "q0"
        },
        "q0100":{
            "": "q0"
        },
        "q0010":{
            "": "q0"
        },
        "q1010":{
            "": "q0"
        },
        "q0000":{
            "": "q0"
        },
        "q0001":{
            "": "q0"
        },
        "q0011":{
            "": "q0"
        }
}

vm_dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
