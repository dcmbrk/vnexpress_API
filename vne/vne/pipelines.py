from itemadapter import ItemAdapter
import mysql.connector

class VnePipeline:


    def open_spider(self, spider):
        #ket noi voi DB
        self.connection = self.get_connect_config(spider)
        self.cursor = self.connection.cursor()

        #Tao bang neu chua co
        create_table = self.create_table_query()
        self.cursor.execute(create_table)
        self.connection.commit()


    def close_spider(self, spider):
        #commit data
        self.connection.commit()
        #dong ket noi
        self.cursor.close()
        self.connection.close()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #Xu li data
        self.strip_field(adapter)
        date = adapter.get('date')
        full_content = self.get_full_content(adapter)
        url = adapter.get('url')


        #Chen data cua bai dang duoc xu li vao DB
        insert_data = self.insert_data_query()
        insert_value = self.insert_value_query(adapter, date, full_content, url)
        self.cursor.execute(insert_data, insert_value)

        return item


#########FUNCTION#########

    def get_connect_config(self, spider):
        """
        CN: Setup config
        """
        return mysql.connector.connect(
            host=spider.settings.get('MYSQL_HOST'),
            user=spider.settings.get('MYSQL_USER'),
            password=spider.settings.get('MYSQL_PASSWORD'),
            database=spider.settings.get('MYSQL_DATABASE')
        )

    def create_table_query(self):
        """
        CN: Query tao bang neu chua co
        """
        return """
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100),
            title TEXT,
            author VARCHAR(255),
            date DATE,
            main_content LONGTEXT,
            url TEXT,
            UNIQUE KEY unique_url (url(255))
        );
        """

    def insert_data_query(self):
        """
        CN: Query quy dinh cac gia tri duoc them
        """
        return """
        INSERT IGNORE INTO articles (category, title, author, date, main_content, url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

    def insert_value_query(self, adapter, date, full_content, url):
        """
        CN: Query quy dinh cac bang duoc them
        """
        return (
            adapter.get('category'),
            adapter.get('title'),
            adapter.get('author'),
            date,
            full_content,
            url
        )

    def get_full_content(self, adapter):
        """
        CN: Tra ve list gop chung cua lead + main_content
        """
        lead = adapter.get('lead', '')
        content_list = adapter.get('main_content', [])
        full_content = ' '.join([lead] + content_list) if isinstance(content_list, list) else lead
        return full_content


    def strip_field(self, adapter):
        """
        CN: Xoa khoang trang tat ca cac field duoc xu li
        """
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()
            elif isinstance(value, list):
                adapter[field_name] = [text.strip() for text in value if isinstance(text, str) and text.strip()]
