source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\marketdata\db\drop_marketdata.sql
source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\staticdata\db\drop_staticdata.sql
source E:\05_Ultimate_Brain\Finance_Skills\HowToQuant\backend\apps\classifiers\db\drop_classifiers.sql

DELETE FROM django_migrations WHERE app in ('staticdata', 'classifiers', 'marketdata');







