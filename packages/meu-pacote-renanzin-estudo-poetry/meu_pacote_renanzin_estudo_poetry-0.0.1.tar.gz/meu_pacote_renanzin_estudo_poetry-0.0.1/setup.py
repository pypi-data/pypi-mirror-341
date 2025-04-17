from setuptools import setup
 
setup(
  name='meu_pacote-renanzin-estudo-poetry',
  version='0.0.1',
  packages=['meu_pacote'],  # Lista de pacotes incluídos no projeto
  install_requires=['httpx'],  # Dependências que serão instaladas junto com o pacote
  entry_points={
      'console_scripts': [
          # Cria um comando chamado "meu-cli" que, ao ser executado no terminal, chama a função `cli` do módulo `meu_pacote.minha_lib`
          'meu-cli = meu_pacote.minha_lib:cli'
      ]
  }
)
