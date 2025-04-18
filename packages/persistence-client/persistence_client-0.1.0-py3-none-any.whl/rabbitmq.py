from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker


exch = RabbitExchange("scraping", auto_delete=True)
queue_save_row = RabbitQueue("save_row", auto_delete=True)
queue_create_data_schema = RabbitQueue("create_data_schema", auto_delete=True)
