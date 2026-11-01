// Fixture with violations (one per linter rule).
let limite = 10
limite = 20                                   // SWF-01

let pontos = 5
if pontos {                                   // SWF-02
    print("ok")
}

if limite > 1 print("no braces")             // SWF-03

let cor = "red"
switch cor {                                  // SWF-04
case "red":
    print("red")
    break                                     // SWF-05
case "blue":
    print("blue")
}

var lista = []                                // SWF-06
var mapa = [:]                                // SWF-06

let largura = 94
let texto = "width: " + largura             // SWF-07
let a = 1
let b = 2.5
let soma = a + b                              // SWF-07

class Animal {
    func falar() -> String { return "..." }
}
class Cao: Animal {
    func falar() -> String { return "au" }    // SWF-08
    override func correr() {}                 // SWF-09
}

class Pessoa {
    var nome: String                          // SWF-10
    var idade: Int
}

struct Contador {
    var n = 0
    func incrementar() {                      // SWF-11
        n += 1
    }
}

enum Falha: Error { case ruim }
func risco() throws -> Int { throw Falha.ruim }
let v = risco()                               // SWF-12

func rede() async -> Int { return 1 }
func chamar() async {
    let x = rede()                            // SWF-13
    print(x)
}

protocol Forma2 {
    var area: Double { get }
    func desenhar()
}
struct Circulo: Forma2 {                      // SWF-14
    var area: Double = 3.14
}

let y = 5;                                    // SWF-15
func main() {}                                // SWF-16

actor Banco {
    var saldo = 0
}
let conta = Banco()
print(conta.saldo)                            // SWF-17

if (limite > 5) {                             // SWF-18
    print("x")
}

var talvez: String? = "oi"
print(talvez.count)                           // SWF-19
let forcado = talvez!                         // SWF-X1
var i = 0
i++                                           // SWF-X2
for (var j = 0; j < 3; j += 1) {              // SWF-X3
    print(j)
}
