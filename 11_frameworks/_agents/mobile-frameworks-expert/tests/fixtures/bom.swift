// Original example (not copied from the tour) using only constructs from A Swift Tour.
let titulo = "Estoque"
var total = 0
let precos: [String: Double] = ["cafe": 12.5, "cha": 8.0]
var nomes: [String] = []
nomes.append("cafe")

for nome in nomes {
    if let preco = precos[nome] {
        print("\(nome) costs \(preco)")
        total += 1
    } else {
        print("no price")
    }
}

var quantidade = 3
let desconto = 0.5
let valor = Double(quantidade) * desconto
print(valor)

enum Nivel: Int {
    case baixo = 1
    case alto
}

switch Nivel.baixo {
case .baixo:
    print("low")
case .alto:
    print("high")
}

let apelido: String? = nil
print(apelido ?? "no nickname")

protocol Descrevivel {
    var descricao: String { get }
    mutating func ajustar()
}

struct Item: Descrevivel {
    var descricao: String = "item"
    mutating func ajustar() {
        descricao += " adjusted"
    }
}

class Forma {
    var lados: Int = 0
    func resumo() -> String {
        return "shape with \(lados) sides"
    }
}

class Quadrado: Forma {
    var lado: Double
    init(lado: Double) {
        self.lado = lado
        super.init()
        lados = 4
    }
    override func resumo() -> String {
        return "square with side \(lado)"
    }
}

enum ErroImpressora: Error {
    case semPapel
}

func enviar(trabalho: Int) throws -> String {
    if trabalho < 0 {
        throw ErroImpressora.semPapel
    }
    return "sent"
}

do {
    let r = try enviar(trabalho: 1)
    print(r)
} catch {
    print(error)
}

func buscar(servidor: String) async -> Int {
    return 1
}

func conectar() async {
    async let a = buscar(servidor: "x")
    print(await a)
    let b = await buscar(servidor: "y")
    print(b)
}

actor Conexao {
    var ativos: [Int] = []
    func registrar(id: Int) {
        ativos.append(id)
    }
}

func usar() async {
    let c = Conexao()
    await c.registrar(id: 1)
}

func primeiro<T: Equatable>(_ a: [T], _ b: T) -> Bool {
    for x in a {
        if x == b {
            return true
        }
    }
    return false
}
