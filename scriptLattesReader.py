#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import csv
import re
import sys
import os, errno, copy, shutil
import datetime 
import string
import operator
from unicodedata import normalize
from collections import namedtuple
from operator import contains
from xml.parsers import expat
from bs4 import BeautifulSoup
from macerrors import noMediaHandler

class QualisArtigosEmPeriodicos:
	nomeArtigo=None
	qualis = None
	origem = None
	def __init__(self):
		self.nomeArtigo=""
		self.qualis =""
		self.origem =""
	
	
class CvLattesProfessorResumo:
	
	ididHC=None
	nome=None
	idLattes=None
	quantidadeOrientacaoMestradoConcluido = None
	quantidadeOrientacaoDoutoradoConcluido = None
	quantidadeOrientacaoIniciacaoCientificaEmAndamento = None
	quantidadeOrientacaoMestradoEmAndamento = None
	quantidadeOrientacaoDoutoradoEmAndamento = None
	quantidadeApresentacaoTrabalho = None
	quantidadeArtigosEmRevista = None
	quantidadeTrabalhoCompletoCongresso = None
	quantidadeArtigosEmPeriodicos = None
	quantidadeProjetosPesquisa = None
	quantidadeParticipacaoEvento = None
	quantidadeLivrosPublicados = None
	quantidadeCapitulosDeLivros = None
	quantidadeProducaoTecnica = None
	
	listaDeQualis =[]
	

	def __init__(self):
		self.idHC=0
		self.nome = ""
		self.idLattes = 0
		self.quantidadeOrientacaoMestradoConcluido = 0
		self.quantidadeOrientacaoDoutoradoConcluido =0
		self.quantidadeOrientacaoIniciacaoCientificaEmAndamento = 0
		self.quantidadeOrientacaoMestradoEmAndamento = 0
		self.quantidadeOrientacaoDoutoradoEmAndamento = 0
		self.quantidadeApresentacaoTrabalho = 0
		self.quantidadeArtigosEmRevista = 0
		self.quantidadeTrabalhoCompletoCongresso = 0
		self.quantidadeArtigosEmPeriodicos = 0
		self.quantidadeProjetosPesquisa = 0
		self.quantidadeParticipacaoEvento = 0
		self.quantidadeLivrosPublicados = 0
		self.quantidadeCapitulosDeLivros = 0
		self.quantidadeProducaoTecnica = 0

	def quantidadeA1(self):
		quantidadeArtigosA1=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'A1':
				quantidadeArtigosA1+=1
		return quantidadeArtigosA1
	
	def quantidadeA2(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'A2':
				quantidadeArtigos+=1
		return quantidadeArtigos
	
	def quantidadeB1(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'B1':
				quantidadeArtigos+=1
		return quantidadeArtigos

	def quantidadeB2(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'B2':
				quantidadeArtigos+=1
		return quantidadeArtigos
	
	def quantidadeB3(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'B3':
				quantidadeArtigos+=1
		return quantidadeArtigos	
	
	def quantidadeB4(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'B4':
				quantidadeArtigos+=1
		return quantidadeArtigos

	def quantidadeB5(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'B5':
				quantidadeArtigos+=1
		return quantidadeArtigos
	
	def quantidadeC1(self):
		quantidadeArtigos=0
		for qualis in self.listaDeQualis:
			if qualis.qualis == 'C1':
				quantidadeArtigos+=1
		return quantidadeArtigos
	
	
def filtraPorPesquisador(artigo, pesquisadorFilter):
	return unicode(artigo[1], encoding='utf-8') == pesquisadorFilter
		
def parseCSVScriptLattes(curriculo, file, separador):
	listaDeArtigos = []
	with open(file,'rb') as csvfile:
		rows = csv.reader(csvfile, delimiter=separador, quoting=csv.QUOTE_NONE)
		for row in rows:
			#print row[0], row[1], row[7]
			artigo = (row[0], row[1], row[7])
			listaDeArtigos+=[artigo]

	listaQualis =[]
	nome = curriculo.nome
	artigosFilter = filter(lambda artigo: filtraPorPesquisador(artigo, nome),listaDeArtigos)
	for artigo in artigosFilter:
		qualis = QualisArtigosEmPeriodicos()
		qualis.qualis = artigo[2]	
		qualis.origem = artigo[0]
		listaQualis+=[qualis]
	curriculo.listaDeQualis=listaQualis		
		
def parseCSVScriptLattesAll(listaDeCurriculos, file, separador):
	listaDeArtigos = []
	with open(file,'rb') as csvfile:
		rows = csv.reader(csvfile, delimiter=separador, quoting=csv.QUOTE_NONE)
		for row in rows:
			#print row[0], row[1], row[7]
			artigo = (row[0], row[1], row[7])
			listaDeArtigos+=[artigo]

	for curriculo in listaDeCurriculos:		
		listaQualis =[]
		nome = curriculo.nome
		artigosFilter = filter(lambda artigo: filtraPorPesquisador(artigo, nome),listaDeArtigos)
		for artigo in artigosFilter:
			qualis = QualisArtigosEmPeriodicos()
			qualis.qualis = artigo[2]	
			qualis.origem = artigo[0]
			listaQualis+=[qualis]
			
		curriculo.listaDeQualis=listaQualis
		
def parseXMLScriptLattesAll(xmlTree):	
	listaDeCurriculos=[]

	for curriculoPesquisador in xmlTree.findAll('pesquisador'):
		curriculo = CvLattesProfessorResumo()
		curriculo.id   = curriculoPesquisador.get('id')
		for identificacao in curriculoPesquisador.findAll('identificacao'):
			curriculo.nome = identificacao.find('nome_completo').string
			
		for participacaoEvento in curriculoPesquisador.findAll('participacao_evento'):
			for evento in participacaoEvento.findAll('evento'):
				curriculo.quantidadeParticipacaoEvento+=1
				
		for trabalhoApresentado in curriculoPesquisador.findAll('apresentacao_trabalho'):
			for trabalho in trabalhoApresentado.findAll('trabalho_apresentado'):
				curriculo.quantidadeApresentacaoTrabalho+=1
				
		for orientacaoIniciacaoCientifica in curriculoPesquisador.findAll('orientacao_iniciacao_cientifica_concluido'):
			for iniciacaoCientifica in orientacaoIniciacaoCientifica.findAll('iniciacao_cientifica'):
				curriculo.quantidadeOrientacaoIniciacaoCientificaEmAndamento+=1	

		for orientacaoMestrado in curriculoPesquisador.findAll('orientacao_mestrado_concluido'):
			for orientacaoConcluida in orientacaoMestrado.findAll('dissertacao'):
				curriculo.quantidadeOrientacaoMestradoConcluido+=1	
				
		for orientacaoMestrado in curriculoPesquisador.findAll('orientacao_mestrado_em_andamento'):
			for orientacaoConcluida in orientacaoMestrado.findAll('dissertacao'):
				curriculo.quantidadeOrientacaoMestradoEmAndamento+=1			

		for orientacaoDoutoradoConcluido in curriculoPesquisador.findAll('orientacao_doutorado_concluido'):
			for tese in orientacaoDoutoradoConcluido.findAll('tese'):
				curriculo.quantidadeOrientacaoDoutoradoConcluido+=1		

		for orientacaoDoutoradoEmAndamento in curriculoPesquisador.findAll('orientacao_doutorado_em_andamento'):
			for tese in orientacaoDoutoradoEmAndamento.findAll('tese'):
				curriculo.quantidadeOrientacaoDoutoradoEmAndamento+=1			

		for projetosDePesquisa in curriculoPesquisador.findAll('projetos_pesquisa'):
			for projeto in projetosDePesquisa.findAll('projeto'):
				curriculo.quantidadeProjetosPesquisa+=1				
		
		for projetosDePesquisa in curriculoPesquisador.findAll('livros_publicados'):
			for livro in projetosDePesquisa.findAll('livro'):
				curriculo.quantidadeLivrosPublicados+=1			
		
		for projetosDePesquisa in curriculoPesquisador.findAll('capitulos_livros'):
			for capitulo in projetosDePesquisa.findAll('capitulo'):
				curriculo.quantidadeCapitulosDeLivros+=1
				
		for projetosDePesquisa in curriculoPesquisador.findAll('producao_tecnica'):
			for producaoTecnica in projetosDePesquisa.findAll('producao'):
				curriculo.quantidadeProducaoTecnica+=1			

				
		listaDeCurriculos = listaDeCurriculos+[curriculo]
	
	return 	listaDeCurriculos

	
def preparXML(path):
	file = open(path)
	page = file.read()
	xmlTree = BeautifulSoup(page, 'xml')
	return xmlTree

def parseXMLScriptLattes(xmlTree):
	list = parseXMLScriptLattesAll(xmlTree)
	return list[0]

def printCurriculos(listaDeCurriculos):
	print '$$$$$$$$$$$$$$$$$$$$$$$$'
	for curriculo in listaDeCurriculos:
		print "pesquisador: ", curriculo.nome,"\n"
		print "id Lattes: ", curriculo.id,"\n"
		print "Quantidade de Participacao em Eventos: ", curriculo.quantidadeParticipacaoEvento,"\n"
		print "Quantidade de Trabalhos Apresentados: ", curriculo.quantidadeApresentacaoTrabalho,"\n"
		print "Quantidade de Orientacao de Mestrado em Andamento: ", curriculo.quantidadeOrientacaoMestradoConcluido ,"\n"
		print "Quantidade de Orientacao de Mestrado Concluido: ", curriculo.quantidadeOrientacaoMestradoConcluido,"\n"
		print "Quantidade de Orientacao de Doutorado em Andamento: ", curriculo.quantidadeOrientacaoDoutoradoEmAndamento,"\n"
		print "Quantidade de Orientacao de Doutorado Concluido: ", curriculo.quantidadeOrientacaoDoutoradoConcluido,"\n"
		print "Quantidade de Orientacao de Iniciacao Cientifica: ", curriculo.quantidadeOrientacaoIniciacaoCientificaEmAndamento,"\n"
		print "Quantidade de Projeto de Pesquisa: ", curriculo.quantidadeOrientacaoIniciacaoCientificaEmAndamento,"\n"
		print "Quantidade de Artigos", len(curriculo.listaDeQualis)
		print "Quantidade de Artigos A1", curriculo.quantidadeA1()	


if __name__ == "__main__":
	
	xmlTree = preparXML('./exemplo/teste-01/teste-01-database.xml')
	#xmlTree = parseXMLScriptLattes(xmlTree)	
	listaDeCurriculos = parseXMLScriptLattesAll(xmlTree)
	printCurriculos(listaDeCurriculos)

	
   
