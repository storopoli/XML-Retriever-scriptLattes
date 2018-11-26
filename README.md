# XML Reader for scriptLattes

A script to get LATTES data from a XML generated by scripLattes

## Getting Started
These instructions will get you up and running.

### 1. Run scriptLattes for a set of Lattes CVs
Run the default scripLattes package to get a XML file for a list of Lattes CVs that you are interested in.

### 2. Run the scripLattesReader.py to generate single Lattes CVs data
```
---------------Example-----------------------
from scriptLattesReader import *
xmlTree = preparXML('./exemplo/teste-01/teste-01-database.xml')
listaDeCurriculos = parseXMLScriptLattesAll(xmlTree)

for cv in listaDeCurriculos:
		print "pesquisador: ", cv.nome
		print "id Lattes: ", cv.id
		print "Quantidade de Artigos", len(curriculo.listaDeQualis) 
		print "Quantidade de Artigos A1", curriculo.quantidadeA1()	
```
## Authors

* **Wonder Alexandre Luz Alvez** - *Creator*
* **Jose Eduardo Storopoli** - *Developer* - [storopoli](https://github.com/storopoli)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
