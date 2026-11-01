# -*- coding: utf-8 -*-
"""
tfjs_map.py - map of tutorials/guide/resources by topic, as NAMED by the captures (it does not bring their content).

Read-only, stdlib, no network. Usage:
  python -I scripts/tfjs_map.py --guide              # 8 guide sections (TFJG p.1)
  python -I scripts/tfjs_map.py --need "converter modelo keras"   # resources for a need (Portuguese or English)
  python -I scripts/tfjs_map.py --all                # full table
  python -I scripts/tfjs_map.py --need "..." --json
Each item carries the citation (CODE p.N). A need with no named resource -> NOT COVERED.
Section and resource titles are quoted as printed in the pt-br captures, with an English gloss.
"""
import argparse
import json
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE = "tensorflow.org/js/guide/"
# (title as printed in the capture, slug, description, English gloss of the title)
GUIA = [
    ("Tensores e Operações", "tensors_operations", "introduction to tensors, data, shapes and data types, TF.js building blocks", "Tensors and Operations"),
    ("Plataforma e Ambiente", "platform_environment", "TF.js platforms and environments and the pros/cons among them", "Platform and Environment"),
    ("Modelos e Camadas", "models_and_layers", "build a model with the Layers API and the Core API", "Models and Layers"),
    ("Treinando Modelos", "train_models", "introduction to training: models, optimizers, loss functions, metrics, variables", "Training Models"),
    ("Salvando e Carregando Modelos", "save_load", "how to save and load TF.js models", "Saving and Loading Models"),
    ("Conversão de Modelo", "conversion", "overview of the model types in the ecosystem and conversion details", "Model Conversion"),
    ("Diferenças do Python tf.keras", "layers_for_keras_users", "differences and capabilities between TF.js and Python tf.keras; JavaScript API conventions", "Differences from Python tf.keras"),
    ("Usando TensorFlow.js no Node.js", "nodejs", "pros/cons among the three Node.js bindings and system requirements", "Using TensorFlow.js in Node.js"),
]

# (topic, keywords [Portuguese + English], resource, what the page says, citations)
MAPA = [
    ("First contact", "primeiro hello world comecar iniciar tutorial primeiros passos minimo first start begin getting started minimal", "Tutorial 'Primeiros passos com o TensorFlow.js' (Getting started with TensorFlow.js; tfjs-examples/getting-started)", "train a minimal model in the browser and predict", "TFJI p.1; TFJL p.9"),
    ("New to ML for the web", "novo iniciante curso video ml aprendizado de maquina web desenvolvedores new beginner course machine learning developers", "Video course 'Aprendizado de máquina para desenvolvedores da Web' (Machine learning for web developers; Google Developers)", "practical introduction to web ML", "TFJI p.3-4; TFJL p.1"),
    ("ML without tensors", "ml5 ml5.js sem tensores otimizadores simples without tensors optimizers simple", "ml5.js library", "built on TF.js, concise and accessible API", "TFJI p.4"),
    ("Install", "instalar instalacao setup configurar npm yarn script tag node install installation configure", "Setup tutorial (tutorials/setup)", "browser and Node.js", "TFJI p.4; TFJS p.1-6"),
    ("Convert a model", "converter conversao keras graphdef saved model python importar pre-treinado convert conversion import pretrained", "Tutorials 'Modelo Keras' (Keras model; import_keras) and 'GraphDef' (import_saved_model); guide 'Conversão de Modelo' (Model Conversion)", "convert pretrained models from Python to TF.js", "TFJI p.4; TFJG p.1; TFJL p.2-3"),
    ("Code examples", "exemplos codigo repositorio github tfjs-examples tarefas examples code repository tasks", "tfjs-examples repository", "small implementations for various ML tasks", "TFJI p.4"),
    ("Visualization", "visualizar visualizacao tfjs-vis grafico comportamento visualize visualization chart behavior", "tfjs-vis (+ MNIST demo)", "in-browser visualization for use with TF.js", "TFJI p.4-5"),
    ("Data", "dados preparar processar data api data prepare process", "API documentation, Data section", "data processing with ML best practices", "TFJI p.5"),
    ("Transfer learning", "transfer learning personalizar retreinar webcam customize retrain", "Tutorial 'What is transfer learning' (tutorials/transfer); webcam controller demo", "customize existing models with your own data", "TFJL p.2-5"),
    ("Ready-made models", "modelos prontos pre-treinados oficiais ready-made pretrained official models", "Page 'Ver modelos' (View models; /js/models)", "pretrained models for common use cases", "TFJL p.1-2"),
    ("Demos", "demos demonstracoes exemplos interativos piano holobooth pac-man demonstrations interactive", "Demos page; Performance RNN; Holobooth; webcam controller", "demos that run in the browser", "TFJL p.2-5"),
    ("Basic concepts (tensors, models, training, save)", "conceitos tensores modelos camadas treino treinar salvar carregar guia concepts tensors models layers training save load guide", "Guide sections (use --guide)", "see the guide table", "TFJG p.1"),
    ("Node.js in depth", "node nodejs ligacoes bindings requisitos requirements", "Guide 'Usando TensorFlow.js no Node.js' (Using TensorFlow.js in Node.js); tfjs-node repository", "pros/cons of the three bindings and requirements", "TFJG p.1; TFJS p.4"),
    ("Use cases / news", "blog noticias casos adobe photoshop moderacao jax news use cases moderation", "TensorFlow blog (posts listed)", "titles and dates only", "TFJL p.5-7"),
    ("Community and help", "ajuda comunidade suporte forum stack overflow github issues sig help community support", "GitHub tfjs, forum, Stack Overflow (tag tensorflow.js), issues, tfjs-announce, SIG, Dev Library", "participation links", "TFJL p.7-8"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def match(need):
    toks = [t for t in re.findall(r"[a-z0-9.]+", norm(need)) if len(t) > 2]
    out = []
    for tema, chaves, rec, diz, cit in MAPA:
        hay = set(re.findall(r"[a-z0-9.]+", norm(tema + " " + chaves)))
        sc = sum(1 for t in toks if t in hay or (len(t) >= 5 and any(w.startswith(t) for w in hay)))
        if sc:
            out.append((sc, tema, rec, diz, cit))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", action="store_true")
    ap.add_argument("--need")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.guide:
        if a.json:
            print(json.dumps([{"n": i + 1, "secao": s, "slug": BASE + g, "descricao": d, "gloss": e, "cite": "TFJG p.1"}
                              for i, (s, g, d, e) in enumerate(GUIA)], ensure_ascii=False, indent=1))
            return 0
        for i, (s, g, d, e) in enumerate(GUIA, 1):
            print(f"{i}. {s} ({e})  ({BASE}{g})  - {d}  [TFJG p.1]")
        print("Section contents: NOT COVERED (the captures only carry the index).")
        return 0
    if a.all:
        for tema, _, rec, diz, cit in MAPA:
            print(f"- {tema}: {rec} - {diz}  [{cit}]")
        return 0
    if a.need:
        m = match(a.need)
        if a.json:
            print(json.dumps([{"tema": t, "recurso": r, "diz": d, "cite": c} for _, t, r, d, c in m], ensure_ascii=False, indent=1))
            return 0
        if not m:
            print("NOT COVERED: no resource named in the captures for this need.")
            return 0
        for _, t, r, d, c in m[:5]:
            print(f"- {t}: {r} - {d}  [{c}]")
        print("Note: the pages only point to these resources; their content is NOT COVERED.")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
