N = 3


def print_instructions():
    print("""
Esse é um simulador simples do Modelo de Hopfield para redes neurais.
Ele armazena um único padrão e testa diversas entradas, mostrando a 
evolução da equação de movimento do modelo.
        
    """)


def verify_input(my_input):
    my_input = [i.strip() for i in my_input[1:-1].split(",")]

    valid = True
    for i in my_input:
        if i != '-1' and i != '1':
            valid = False

    return valid


def convert(pat):
    return [int(i.strip()) for i in pat[1:-1].split(",")]


def read_pattern(text, default=None):
    my_input = ""

    while not verify_input(my_input):
        my_input = input(text)
        if default and my_input == "":
            my_input = default

    return convert(my_input)


def calc(pat, i, j):
    cte = 1 / N

    if i == j:
        return 0
    else:
        return cte * pat[i] * pat[j]


def calculate_weights(pat):
    w = N * [None]
    for i in range(N):
        w[i] = N * [None]
        for j in range(N):
            w[i][j] = calc(pat, i, j)

    return w


def select_method():
    met = None
    while met != 'S' and met != 'A':
        met = input("Por favor selecione o método de atualização:\n(s|S) Síncrono\n(a|A) Assíncrono\n")
        met = met.strip().upper()

    return met


def print_all():
    print("\n##################")
    print(f"Padrão armazenado: {pattern}")
    print(f"Matriz de pesos: {weights}")
    print(f"Método selecionado para atualização: {method}")
    print(f"Estado inicial a ser avaliado: {initial_state}")
    print("##################\n")


def signal(x):
    if x >= 0:
        return 1
    else:
        return -1


def sync_evaluate(start, w):
    t = 0
    s = [start, N * [None]]

    t += 1
    while t - 2 < 0 or s[t - 1] != s[t - 2]:
        s[t][0] = signal(w[0][1] * s[t - 1][1] + w[0][2] * s[t - 1][2])
        print(f"S0({t}) = sgn(w01*s1({t - 1}) + w02*s2({t - 1}))")
        print(f"S0({t}) = sgn({w[0][1] * s[t - 1][1]} + {w[0][2] * s[t - 1][2]}) = {s[t][0]}")

        s[t][1] = signal(w[1][0] * s[t - 1][0] + w[1][2] * s[t - 1][2])
        print(f"S1({t}) = sgn(w10*s0({t - 1}) + w12*s2({t - 1}))")
        print(f"S1({t}) = sgn({w[1][0] * s[t - 1][0]} + {w[1][2] * s[t - 1][2]}) = {s[t][1]}")

        s[t][2] = signal(w[2][0] * s[t - 1][0] + w[2][1] * s[t - 1][1])
        print(f"S2({t}) = sgn(w20*s0({t - 1}) + w21*s1({t - 1}))")
        print(f"S2({t}) = sgn({w[2][0] * s[t - 1][0]} + {w[2][1] * s[t - 1][1]}) = {s[t][2]}")

        t += 1
        s.append(N * [None])

        print(f"\nEstados: {s}")
        print(f"t = {t}")
        input()


def async_evaluate(start, w):
    t = 0
    s = [start, N * [None]]

    t += 1
    while t - 2 < 0 or s[t - 1] != s[t - 4]:
        s[t][0] = signal(w[0][1] * s[t - 1][1] + w[0][2] * s[t - 1][2])
        print(f"S0({t}) = sgn(w01*s1({t - 1}) + w02*s2({t - 1}))")
        print(f"S0({t}) = sgn({w[0][1] * s[t - 1][1]} + {w[0][2] * s[t - 1][2]}) = {s[t][0]}")
        s[t][1] = s[t - 1][1]
        s[t][2] = s[t - 1][2]
        t += 1
        s.append(N * [None])

        s[t][0] = s[t - 1][0]
        s[t][1] = signal(w[1][0] * s[t - 1][0] + w[1][2] * s[t - 1][2])
        print(f"S1({t}) = sgn(w10*s0({t - 1}) + w12*s2({t - 1}))")
        print(f"S1({t}) = sgn({w[1][0] * s[t - 1][0]} + {w[1][2] * s[t - 1][2]}) = {s[t][1]}")
        s[t][2] = s[t - 1][2]
        t += 1
        s.append(N * [None]);

        s[t][0] = s[t - 1][0]
        s[t][1] = s[t - 1][1]
        s[t][2] = signal(w[2][0] * s[t - 1][0] + w[2][1] * s[t - 1][1])
        print(f"S2({t}) = sgn(w20*s0({t - 1}) + w21*s1({t - 1}))")
        print(f"S2({t}) = sgn({w[2][0] * s[t - 1][0]} + {w[2][1] * s[t - 1][1]}) = {s[t][2]}")
        t += 1
        s.append(N * [None])

        print(f"Estados: {s}")
        print(f"t = {t}")
        input()


if __name__ == '__main__':
    print_instructions()
    pattern = read_pattern("Insira um padrão no formato (a, b, c), aonde a, b e c podem ser -1 ou 1.\n"
                           "Por exemplo (-1, 1, 1):\n", default="(-1, 1, 1)")
    weights = calculate_weights(pattern)
    method = select_method()
    initial_state = read_pattern("Insira um estado inicial a ser pesquisado.\n"
                                 "Por exemplo (-1, -1, -1):\n", default="(-1, -1, -1)")
    print_all()
    if method == "S":
        sync_evaluate(initial_state, weights)
    else:
        async_evaluate(initial_state, weights)
