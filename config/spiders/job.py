import scrapy

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['quera.org']
    start_urls = ['https://quera.org/magnet/jobs']

    def parse(self, response):
        for page_index in range(1,6):
            page = f"https://quera.org/magnet/jobs?page={page_index}"
            yield scrapy.Request(url=page,callback=self.parse_page)

    def parse_page(self, response):
        jobs = response.xpath('//div[@class="chakra-stack css-1qgzdoz"]/div/a')

        for job in jobs:
            url = f"https://quera.org{job.xpath('.//@href').get()}"
            yield scrapy.Request(url=url,callback=self.parse_job)
    
    def parse_job(self, response):
        title = response.xpath("//h1[@class='chakra-heading css-17g3d1']/text()").get()
        
        gender = None
        if title.lower().__contains__("آقا") or title.lower().__contains__("male"):gender = 'male'
        elif title.lower().__contains__("خانم") or title.lower().__contains__("female"): gender = 'female'

        city = response.xpath('(//div[@class="chakra-stack css-84zodg"]/span/text())[1]').get()
        url = response.request.url
      
        education = None

        insurance = False
        if response.xpath('(//ul[@class="chakra-wrap__list css-wah4g8"])[2]/descendant::node()[contains(text(),"بیمه")]') :
            insurance = True

        cooperation = response.xpath('(//div[@class="chakra-stack css-o5l3sd"]/div/div[@class="css-vlgdo0"]/p)[1]/text()').get()

        salary = response.xpath('//div[@class="chakra-stack css-o5l3sd"]/div[@class="chakra-stack css-r0tra5"]/p/following-sibling::div/p/text()').get()
        if not salary : salary = -1
        elif salary.__contains__("تا") : salary = salary.split('تا')[0]

        experience = -1
        experience_text = response.xpath('//div[@class="css-rmlqu9"]/descendant::node()[contains(text(),"سال سابقه")]/text()').get()
        experience_text2 = response.xpath('//div[@class="css-rmlqu9"]/div/p[contains(text(),"سال سابقه")]/text()').get()
        if experience_text:
            for m in experience_text:
                if m.isdigit():
                    experience = m
                    break
        elif experience_text2 :
            for m in experience_text2:
                if m.isdigit():
                    experience = m
                    break

        teleworking = False 
        if response.xpath("//span[contains(text(),'امکان دورکاری')]") : teleworking = True

        yield {
            'title' : title,
            'city' : city,
            'education' : education,
            'insurance' : insurance,
            'cooperation' : cooperation,
            'salary' : salary,
            'gender' : gender,
            'experience' : experience,
            'teleworking' : teleworking,
            'url' : url,
        }        