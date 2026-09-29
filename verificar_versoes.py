import sys
from importlib.metadata import version, PackageNotFoundError

libs_projeto = [
    'streamlit', 'pandas', 'numpy', 'scikit-learn', 
    'joblib', 'plotly', 'pyarrow', 'seaborn', 'matplotlib'
]

print("="*60)
print(f"🐍 VERSÃO DO PYTHON LOCAL: {sys.version.split()[0]}")
print("="*60)
print("🔍 VERIFICAÇÃO DE BIBLIOTECAS NO AMBIENTE LOCAL")
print("="*60)

for lib in libs_projeto:
    try:
        v = version(lib)
        print(f"  ✅ {lib:<15} == {v}")
    except PackageNotFoundError:
        print(f"  ❌ {lib:<15} -> NÃO INSTALADA")

print("="*60)