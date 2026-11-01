// Code with the same structure as the tour examples (names changed); must not produce findings.
var quantidade = 42
let rotulo = "The width is "
let largura = 94
let rotuloLargura = rotulo + String(largura)
let maca = 3
let resumo = "I have \(maca) apples."
var frutas = ["a", "b"]
frutas[1] = "c"
let vazio: [String] = []
let vazioMapa: [String: Float] = [:]

let notas = [75, 43, 103]
var time = 0
for nota in notas {
    if nota > 50 {
        time += 3
    } else {
        time += 1
    }
}
let enfeite = if time > 10 {
    "!"
} else {
    ""
}

var nomeOpcional: String? = "Ana"
var saudacao = "Hello!"
if let nome = nomeOpcional {
    saudacao = "Hello, \(nome)"
}
let apelido: String? = nil
let completo: String = "Ana"
let informal = "Hi \(apelido ?? completo)"
if let apelido {
    print("Hey, \(apelido)")
}

let legume = "pimenta"
switch legume {
case "aipo":
    print("aipo")
case let x where x.hasSuffix("pimenta"):
    print("is it spicy? \(x)")
default:
    print("all good")
}

var n = 2
while n < 100 {
    n *= 2
}
var m = 2
repeat {
    m *= 2
} while m < 100
var soma = 0
for i in 0..<4 {
    soma += i
}

func cumprimentar(_ pessoa: String, em dia: String) -> String {
    return "Hello \(pessoa), today is \(dia)."
}

func estatisticas(notas: [Int]) -> (min: Int, max: Int, sum: Int) {
    var min = notas[0]
    var max = notas[0]
    var sum = 0
    for nota in notas {
        if nota > max {
            max = nota
        } else if nota < min {
            min = nota
        }
        sum += nota
    }
    return (min, max, sum)
}

func tem(lista: [Int], condicao: (Int) -> Bool) -> Bool {
    for item in lista {
        if condicao(item) {
            return true
        }
    }
    return false
}
let triplos = notas.map({ numero in 3 * numero })
let ordenados = notas.sorted { $0 > $1 }

class Forma {
    var lados: Int = 0
    var nome: String
    init(nome: String) {
        self.nome = nome
    }
    deinit {
        print("end")
    }
    func descricao() -> String {
        return "shape with \(lados) sides"
    }
}

class Quadrado: Forma {
    var lado: Double
    init(lado: Double, nome: String) {
        self.lado = lado
        super.init(nome: nome)
        lados = 4
    }
    func area() -> Double {
        return lado * lado
    }
    override func descricao() -> String {
        return "square"
    }
}

class Triangulo: Forma {
    var lado: Double = 0.0
    init(lado: Double, nome: String) {
        self.lado = lado
        super.init(nome: nome)
        lados = 3
    }
    var perimetro: Double {
        get {
            return 3.0 * lado
        }
        set {
            lado = newValue / 3.0
        }
    }
}

class Par {
    var triangulo: Triangulo {
        willSet {
            quadrado.lado = newValue.lado
        }
    }
    var quadrado: Quadrado {
        willSet {
            triangulo.lado = newValue.lado
        }
    }
    init(tamanho: Double, nome: String) {
        quadrado = Quadrado(lado: tamanho, nome: nome)
        triangulo = Triangulo(lado: tamanho, nome: nome)
    }
}

enum Valor: Int {
    case as = 1
    case dois, tres
    func descricao() -> String {
        switch self {
        case .as:
            return "as"
        default:
            return String(self.rawValue)
        }
    }
}

enum Resposta {
    case resultado(String, String)
    case falha(String)
}
let ok = Resposta.resultado("6:00", "20:09")
switch ok {
case let .resultado(nascer, por):
    print("\(nascer) \(por)")
case let .falha(mensagem):
    print(mensagem)
}

struct Carta {
    var valor: Valor
    func descricao() -> String {
        return "card"
    }
}

func buscarID(servidor: String) async -> Int {
    if servidor == "primario" {
        return 97
    }
    return 501
}

func conectar(servidor: String) async {
    async let id = buscarID(servidor: servidor)
    let saudacao = "id \(await id)"
    print(saudacao)
}

Task {
    await conectar(servidor: "primario")
}

actor Servidor {
    var ativos: [Int] = []
    func conectar() async -> Int {
        let id = await buscarID(servidor: "x")
        ativos.append(id)
        return id
    }
}

protocol Exemplo {
    var descricao: String { get }
    mutating func ajustar()
}

class Simples: Exemplo {
    var descricao: String = "simple"
    func ajustar() {
        descricao += " adjusted"
    }
}

struct Estrutura: Exemplo {
    var descricao: String = "structure"
    mutating func ajustar() {
        descricao += " adjusted"
    }
}

extension Int: Exemplo {
    var descricao: String {
        return "The number \(self)"
    }
    mutating func ajustar() {
        self += 42
    }
}

enum ErroImpressora: Error {
    case semPapel, semToner, fogo
}

func enviar(trabalho: Int, para impressora: String) throws -> String {
    if impressora == "Sem Toner" {
        throw ErroImpressora.semToner
    }
    return "sent"
}

do {
    let resposta = try enviar(trabalho: 1040, para: "Bi")
    print(resposta)
} catch ErroImpressora.fogo {
    print("fogo")
} catch let erro as ErroImpressora {
    print(erro)
} catch {
    print(error)
}
let sucesso = try? enviar(trabalho: 1884, para: "M")

var geladeiraAberta = false
func geladeiraTem(_ comida: String) -> Bool {
    geladeiraAberta = true
    defer {
        geladeiraAberta = false
    }
    return ["leite"].contains(comida)
}

func fazerArray<Item>(repetindo item: Item, vezes: Int) -> [Item] {
    var resultado: [Item] = []
    for _ in 0..<vezes {
        resultado.append(item)
    }
    return resultado
}

func algumComum<T: Sequence, U: Sequence>(_ a: T, _ b: U) -> Bool
    where T.Element: Equatable, T.Element == U.Element
{
    for x in a {
        for y in b {
            if x == y {
                return true
            }
        }
    }
    return false
}
