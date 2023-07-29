import scrapy

class BagucinhaguiSpider(scrapy.Spider):
    name = "bagucinhagui"
    start_urls = ["https://www.arquidiocesedefortaleza.org.br/regioes/"]
    selector_menu_em_cima = '#content-title .page_item_has_children a'
    i = 0

    def parse(self, response):
        #links para visitar
        links_arquidioceses = response.css(self.selector_menu_em_cima).xpath("@href").getall()

        for links in links_arquidioceses:
            yield scrapy.Request(links, self.parse_item)


    def parse_item(self, response):
        #clicando na palavra Paróquias da Região
        paroquias_regiao_pag = response.css('#content-page .page_item_has_children > a').xpath("@href").getall()
        paroquias_regiao_pag = self.retira_links_indesejados(paroquias_regiao_pag)
        yield scrapy.Request(paroquias_regiao_pag[0], self.parse_paroquias)

    def parse_paroquias(self, response):
        # itens do menu
        paroquias_itens_menu = response.css('#content-page .page_item a').xpath("@href").getall()

        for url_especifico in paroquias_itens_menu:
            yield scrapy.Request(url_especifico, self.pegar_dados_paroquia)


    def pegar_dados_paroquia(self, response):
        nome_paroquia = response.css('.page-title::text').getall()
        cep = response.css(".is-style-stripes:nth-child(3) tr:nth-child(3) td+ td::text").getall()
        endereco = response.css(".is-style-stripes:nth-child(3) tr:nth-child(1) td+ td::text").getall()
        if cep == []:
            cep = response.css(".page-title+ .is-style-stripes tr:nth-child(3) td+ td::text").getall()
        if cep == []:
            cep = response.css(".is-style-stripes:nth-child(2) tr:nth-child(3) td+ td::text").getall()
        if cep == []:
            cep = response.css(".wp-container-2 tr:nth-child(3) td+ td::text").getall()
        if endereco == []:
            endereco = response.css(".page-title+ .is-style-stripes tr:nth-child(1) td+ td::text").getall()
        if endereco == []:
            endereco = response.css(".is-style-stripes:nth-child(2) tr:nth-child(1) td+ td::text").getall()
        if endereco == []:
            endereco = response.css(".wp-container-2 tr:nth-child(1) td+ td:text").getall()

        bairro = response.css(".is-style-stripes:nth-child(3) tr:nth-child(2) td+ td::text").getall()
        if bairro == []:
            bairro = response.css(".is-style-stripes:nth-child(2) tr:nth-child(2) td+ td::text").getall()

        if bairro == []:
            bairro = response.css(".wp-container-2 tr:nth-child(2) td+ td::text").getall()

        horario_missa_domingo = response.css(".is-style-stripes:nth-child(7) tr:nth-child(1) td+ td::text").getall()
        horario_missa_segunda = response.css(".is-style-stripes:nth-child(7) tr:nth-child(2) td+ td::text").getall()
        horario_missa_terca = response.css(".is-style-stripes:nth-child(7) tr:nth-child(3) td+ td::text").getall()
        horario_missa_quarta = response.css(".is-style-stripes:nth-child(7) tr:nth-child(4) td+ td::text").getall()
        horario_missa_quinta = response.css(".is-style-stripes:nth-child(7) tr:nth-child(5) td+ td::text").getall()
        horario_missa_sexta = response.css(".is-style-stripes:nth-child(7) tr:nth-child(6) td+ td::text").getall()
        horario_missa_sabado = response.css(".is-style-stripes:nth-child(7) tr:nth-child(7) td+ td::text").getall()
        horario_confissoes = response.css(".has-medium-font-size+ p::text").getall()

        yield {
            "nome": nome_paroquia,
            "cep": cep,
            "endereco": endereco,
            "bairro": bairro,
            "horario_missa_domingo" : horario_missa_domingo,
            "horario_missa_segunda" : horario_missa_segunda,
            "horario_missa_terca" : horario_missa_terca,
            "horario_missa_quarta" : horario_missa_quarta,
            "horario_missa_quinta" : horario_missa_quinta,
            "horario_missa_sexta" : horario_missa_sexta,
            "horario_missa_sabado" : horario_missa_sabado,
            "horario_confissoes" : horario_confissoes
        }

    def retira_links_indesejados(self, lista):
        palavra_a_remover = "mapa-da-regiao"
        minha_lista = [item for item in lista if palavra_a_remover not in item]
        return minha_lista





