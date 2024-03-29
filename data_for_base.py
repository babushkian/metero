from datetime import date, datetime
meters = [
	{"id":2, "name":"кукуруза", "user_id":2, "order":2},
	{"id":3, "name":"суп", "user_id":2, "order":3},
	{"id":6, "name":"ничевок", "user_id":1, "order":2},
	{"id":7, "name":"лупонюшка", "user_id":1, "order":1},
	{"id":8, "name":"поняшка", "user_id":1, "order":3},
	{"id":12, "name":"огонь", "user_id":3, "order":2},
	{"id":13, "name":"вода", "user_id":3, "order":1},
	{"id":14, "name":"холодная труба", "user_id":3, "order":3},
	{"id":15, "name":"горячая труба", "user_id":3, "order":4},
	{"id":16, "name":"псина", "user_id":4, "order":3},
	{"id":17, "name":"котик", "user_id":4, "order":4},
	{"id":18, "name":"белочка", "user_id":4, "order":1},
	{"id":20, "name":"кабачок", "user_id":2, "order":4},
	{"id":21, "name":"коляска", "user_id":2, "order":1},
	{"id":27, "name":"волчара", "user_id":4, "order":5},
	{"id":34, "name":"пышка", "user_id":1, "order":7},
	{"id":39, "name":"зарплаты с каждым годом растут", "user_id":3, "order":5},
	{"id":40, "name":"улыбняшка", "user_id":1, "order":8},
]
users = [
	{"id":1, "name":"Дмитрий", "email":"dimba@mail.ru", "psw":"pbkdf2:sha256:600000$Iwfln0LReXQBIe5i$a9c4fd539473cf0a5c80973563a788e80c804d04d865fbbed452d8a51bf483b7", "date":datetime(2023, 9, 27, 12, 0, 51)},
	{"id":2, "name":"Константин", "email":"kos@mail.ru", "psw":"pbkdf2:sha256:600000$Y5jGerm0lhLnymSZ$f976cfd4864b34f169ce427c16467f0ff7987dba664b0dffc732d21222b0579b", "date":datetime(2023, 9, 27, 12, 1, 13)},
	{"id":3, "name":"Fake", "email":"f@f.ru", "psw":"pbkdf2:sha256:600000$Et9NMMx0NadiF0MG$5920ddd98ae277ee99574429eccc71ac5dc03b575230dbb26be11615013d59d6", "date":datetime(2023, 9, 27, 16, 58, 7)},
	{"id":4, "name":"Вася", "email":"vas@mail.ru", "psw":"pbkdf2:sha256:600000$vykEPj5lfzF71sJE$fe3458ba82a0b9471eb13975d462b8dc8e34070c564bfb533470a50d765c2165", "date":datetime(2023, 9, 28, 9, 6, 26)},
]

measures = [
	{"id":2, "user_id":2, "meter_id":2, "date_id":5, "data":1.0},
	{"id":3, "user_id":2, "meter_id":3, "date_id":5, "data":1.0},
	{"id":7, "user_id":2, "meter_id":2, "date_id":6, "data":1.0},
	{"id":8, "user_id":2, "meter_id":3, "date_id":6, "data":2.0},
	{"id":12, "user_id":1, "meter_id":6, "date_id":7, "data":21.0},
	{"id":13, "user_id":1, "meter_id":7, "date_id":7, "data":14.0},
	{"id":14, "user_id":1, "meter_id":8, "date_id":7, "data":343.0},
	{"id":16, "user_id":1, "meter_id":6, "date_id":8, "data":12.0},
	{"id":17, "user_id":1, "meter_id":7, "date_id":8, "data":13.0},
	{"id":18, "user_id":1, "meter_id":8, "date_id":8, "data":14.0},
	{"id":20, "user_id":1, "meter_id":6, "date_id":9, "data":1.0},
	{"id":21, "user_id":1, "meter_id":7, "date_id":9, "data":2.0},
	{"id":22, "user_id":1, "meter_id":8, "date_id":9, "data":3.0},
	{"id":25, "user_id":3, "meter_id":12, "date_id":10, "data":13.0},
	{"id":26, "user_id":3, "meter_id":13, "date_id":10, "data":225.0},
	{"id":27, "user_id":3, "meter_id":14, "date_id":10, "data":8.0},
	{"id":28, "user_id":3, "meter_id":15, "date_id":10, "data":15.0},
	{"id":30, "user_id":2, "meter_id":2, "date_id":11, "data":345.0},
	{"id":31, "user_id":2, "meter_id":3, "date_id":11, "data":567.0},
	{"id":35, "user_id":1, "meter_id":6, "date_id":12, "data":12.0},
	{"id":36, "user_id":1, "meter_id":7, "date_id":12, "data":12.0},
	{"id":37, "user_id":1, "meter_id":8, "date_id":12, "data":14.0},
	{"id":40, "user_id":1, "meter_id":6, "date_id":13, "data":21.0},
	{"id":41, "user_id":1, "meter_id":7, "date_id":13, "data":22.0},
	{"id":42, "user_id":1, "meter_id":8, "date_id":13, "data":23.0},
	{"id":45, "user_id":1, "meter_id":6, "date_id":14, "data":12.0},
	{"id":46, "user_id":1, "meter_id":7, "date_id":14, "data":13.0},
	{"id":47, "user_id":1, "meter_id":8, "date_id":14, "data":14.0},
	{"id":51, "user_id":3, "meter_id":12, "date_id":15, "data":15.0},
	{"id":52, "user_id":3, "meter_id":13, "date_id":15, "data":5432.0},
	{"id":53, "user_id":3, "meter_id":14, "date_id":15, "data":66.0},
	{"id":54, "user_id":3, "meter_id":15, "date_id":15, "data":99.0},
	{"id":55, "user_id":3, "meter_id":12, "date_id":16, "data":16.0},
	{"id":56, "user_id":3, "meter_id":13, "date_id":16, "data":5555.0},
	{"id":57, "user_id":3, "meter_id":14, "date_id":16, "data":77.0},
	{"id":58, "user_id":3, "meter_id":15, "date_id":16, "data":101.0},
	{"id":60, "user_id":2, "meter_id":2, "date_id":17, "data":23.0},
	{"id":61, "user_id":2, "meter_id":3, "date_id":17, "data":34.0},
	{"id":65, "user_id":2, "meter_id":20, "date_id":17, "data":78.0},
	{"id":66, "user_id":2, "meter_id":21, "date_id":17, "data":89.0},
	{"id":72, "user_id":2, "meter_id":2, "date_id":1, "data":54.0},
	{"id":73, "user_id":2, "meter_id":3, "date_id":1, "data":12.0},
	{"id":77, "user_id":2, "meter_id":20, "date_id":1, "data":52.0},
	{"id":78, "user_id":2, "meter_id":21, "date_id":1, "data":56.0},
	{"id":84, "user_id":4, "meter_id":16, "date_id":19, "data":123.0},
	{"id":85, "user_id":4, "meter_id":17, "date_id":19, "data":234.0},
	{"id":86, "user_id":4, "meter_id":18, "date_id":19, "data":345.0},
	{"id":87, "user_id":4, "meter_id":16, "date_id":20, "data":12.0},
	{"id":88, "user_id":4, "meter_id":17, "date_id":20, "data":23.0},
	{"id":89, "user_id":4, "meter_id":18, "date_id":20, "data":34.0},
	{"id":90, "user_id":4, "meter_id":16, "date_id":21, "data":123.0},
	{"id":91, "user_id":4, "meter_id":17, "date_id":21, "data":234.0},
	{"id":92, "user_id":4, "meter_id":18, "date_id":21, "data":345.0},
	{"id":93, "user_id":4, "meter_id":27, "date_id":21, "data":567.0},
	{"id":94, "user_id":4, "meter_id":16, "date_id":22, "data":44.0},
	{"id":95, "user_id":4, "meter_id":17, "date_id":22, "data":55.0},
	{"id":96, "user_id":4, "meter_id":18, "date_id":22, "data":12.0},
	{"id":97, "user_id":4, "meter_id":27, "date_id":22, "data":233.0},
	{"id":99, "user_id":4, "meter_id":16, "date_id":23, "data":11.0},
	{"id":100, "user_id":4, "meter_id":17, "date_id":23, "data":22.0},
	{"id":101, "user_id":4, "meter_id":18, "date_id":23, "data":33.0},
	{"id":102, "user_id":4, "meter_id":27, "date_id":23, "data":44.0},
	{"id":104, "user_id":4, "meter_id":16, "date_id":30, "data":999.0},
	{"id":105, "user_id":4, "meter_id":17, "date_id":30, "data":999.0},
	{"id":106, "user_id":4, "meter_id":18, "date_id":30, "data":999.0},
	{"id":107, "user_id":4, "meter_id":27, "date_id":30, "data":999.0},
	{"id":109, "user_id":4, "meter_id":16, "date_id":31, "data":123.0},
	{"id":110, "user_id":4, "meter_id":17, "date_id":31, "data":111.0},
	{"id":111, "user_id":4, "meter_id":18, "date_id":31, "data":222.0},
	{"id":112, "user_id":4, "meter_id":27, "date_id":31, "data":999.0},
	{"id":114, "user_id":1, "meter_id":6, "date_id":30, "data":1.0},
	{"id":115, "user_id":1, "meter_id":7, "date_id":30, "data":1.0},
	{"id":116, "user_id":1, "meter_id":8, "date_id":30, "data":1.0},
	{"id":120, "user_id":1, "meter_id":6, "date_id":31, "data":2.0},
	{"id":121, "user_id":1, "meter_id":7, "date_id":31, "data":2.0},
	{"id":122, "user_id":1, "meter_id":8, "date_id":31, "data":2.0},
	{"id":126, "user_id":1, "meter_id":6, "date_id":32, "data":3.0},
	{"id":127, "user_id":1, "meter_id":7, "date_id":32, "data":4.0},
	{"id":128, "user_id":1, "meter_id":8, "date_id":32, "data":5.0},
	{"id":132, "user_id":3, "meter_id":12, "date_id":33, "data":17.0},
	{"id":133, "user_id":3, "meter_id":13, "date_id":33, "data":5666.0},
	{"id":134, "user_id":3, "meter_id":14, "date_id":33, "data":88.0},
	{"id":135, "user_id":3, "meter_id":15, "date_id":33, "data":103.0},
	{"id":137, "user_id":2, "meter_id":2, "date_id":30, "data":2.0},
	{"id":138, "user_id":2, "meter_id":3, "date_id":30, "data":3.0},
	{"id":142, "user_id":2, "meter_id":20, "date_id":30, "data":7.0},
	{"id":143, "user_id":2, "meter_id":21, "date_id":30, "data":8.0},
	{"id":150, "user_id":2, "meter_id":2, "date_id":31, "data":1.0},
	{"id":151, "user_id":2, "meter_id":3, "date_id":31, "data":1.0},
	{"id":155, "user_id":2, "meter_id":20, "date_id":31, "data":1.0},
	{"id":156, "user_id":2, "meter_id":21, "date_id":31, "data":1.0},
	{"id":165, "user_id":1, "meter_id":6, "date_id":35, "data":1.0},
	{"id":166, "user_id":1, "meter_id":7, "date_id":35, "data":2.0},
	{"id":167, "user_id":1, "meter_id":8, "date_id":35, "data":3.0},
	{"id":171, "user_id":1, "meter_id":6, "date_id":36, "data":1.0},
	{"id":172, "user_id":1, "meter_id":7, "date_id":36, "data":34.0},
	{"id":173, "user_id":1, "meter_id":8, "date_id":36, "data":56.0},
	{"id":190, "user_id":3, "meter_id":12, "date_id":40, "data":123.0},
	{"id":191, "user_id":3, "meter_id":13, "date_id":40, "data":234.0},
	{"id":192, "user_id":3, "meter_id":14, "date_id":40, "data":345.0},
	{"id":193, "user_id":3, "meter_id":15, "date_id":40, "data":567.0},
	{"id":194, "user_id":3, "meter_id":39, "date_id":40, "data":678.0},
	{"id":195, "user_id":1, "meter_id":6, "date_id":38, "data":66.0},
	{"id":196, "user_id":1, "meter_id":7, "date_id":38, "data":37.0},
	{"id":197, "user_id":1, "meter_id":8, "date_id":38, "data":111.0},
	{"id":198, "user_id":1, "meter_id":34, "date_id":38, "data":8.0},
	{"id":199, "user_id":1, "meter_id":6, "date_id":41, "data":12.0},
	{"id":200, "user_id":1, "meter_id":7, "date_id":41, "data":32.0},
	{"id":201, "user_id":1, "meter_id":8, "date_id":41, "data":54.0},
	{"id":202, "user_id":1, "meter_id":34, "date_id":41, "data":333.0},
	{"id":204, "user_id":1, "meter_id":6, "date_id":42, "data":31.0},
	{"id":205, "user_id":1, "meter_id":7, "date_id":42, "data":31.0},
	{"id":206, "user_id":1, "meter_id":8, "date_id":42, "data":31.0},
	{"id":207, "user_id":1, "meter_id":34, "date_id":42, "data":31.0},
	{"id":209, "user_id":1, "meter_id":6, "date_id":43, "data":0.0},
	{"id":210, "user_id":1, "meter_id":7, "date_id":43, "data":0.0},
	{"id":211, "user_id":1, "meter_id":8, "date_id":43, "data":0.0},
	{"id":212, "user_id":1, "meter_id":34, "date_id":43, "data":0.0},
	{"id":213, "user_id":1, "meter_id":40, "date_id":43, "data":0.0},
	{"id":214, "user_id":3, "meter_id":12, "date_id":37, "data":11.0},
	{"id":215, "user_id":3, "meter_id":13, "date_id":37, "data":2.0},
	{"id":216, "user_id":3, "meter_id":14, "date_id":37, "data":3.0},
	{"id":217, "user_id":3, "meter_id":15, "date_id":37, "data":4.0},
	{"id":218, "user_id":3, "meter_id":39, "date_id":37, "data":2.0},
	{"id":219, "user_id":3, "meter_id":12, "date_id":44, "data":1.0},
	{"id":220, "user_id":3, "meter_id":13, "date_id":44, "data":2.0},
	{"id":221, "user_id":3, "meter_id":14, "date_id":44, "data":2.0},
	{"id":222, "user_id":3, "meter_id":15, "date_id":44, "data":2.0},
	{"id":223, "user_id":3, "meter_id":39, "date_id":44, "data":2.0},
	{"id":224, "user_id":3, "meter_id":13, "date_id":45, "data":1.0},
	{"id":225, "user_id":3, "meter_id":12, "date_id":45, "data":1.0},
	{"id":226, "user_id":3, "meter_id":14, "date_id":45, "data":1.0},
	{"id":227, "user_id":3, "meter_id":15, "date_id":45, "data":1.0},
	{"id":228, "user_id":3, "meter_id":39, "date_id":45, "data":1.0},
]
dates = [
	{"id":1, "date":date(2023, 9, 8)},
	{"id":2, "date":date(2023, 8, 31)},
	{"id":3, "date":date(2023, 9, 16)},
	{"id":4, "date":date(2023, 9, 19)},
	{"id":5, "date":date(2023, 9, 7)},
	{"id":6, "date":date(2023, 9, 6)},
	{"id":7, "date":date(2023, 9, 1)},
	{"id":8, "date":date(2023, 4, 12)},
	{"id":9, "date":date(2023, 9, 17)},
	{"id":10, "date":date(2020, 1, 1)},
	{"id":11, "date":date(2023, 6, 1)},
	{"id":12, "date":date(2023, 9, 9)},
	{"id":13, "date":date(2023, 8, 26)},
	{"id":14, "date":date(2023, 9, 27)},
	{"id":15, "date":date(2021, 1, 1)},
	{"id":16, "date":date(2022, 1, 1)},
	{"id":17, "date":date(2023, 4, 5)},
	{"id":18, "date":date(2023, 9, 10)},
	{"id":19, "date":date(2023, 8, 10)},
	{"id":20, "date":date(2023, 9, 15)},
	{"id":21, "date":date(2023, 5, 10)},
	{"id":22, "date":date(2021, 2, 1)},
	{"id":23, "date":date(2021, 3, 1)},
	{"id":24, "date":date(2021, 3, 2)},
	{"id":25, "date":date(2023, 10, 13)},
	{"id":26, "date":date(2023, 10, 17)},
	{"id":27, "date":date(2023, 10, 22)},
	{"id":28, "date":date(2023, 9, 2)},
	{"id":29, "date":date(2023, 10, 26)},
	{"id":30, "date":date(2023, 10, 7)},
	{"id":31, "date":date(2023, 10, 8)},
	{"id":32, "date":date(2023, 10, 9)},
	{"id":33, "date":date(2023, 1, 1)},
	{"id":34, "date":date(2023, 12, 28)},
	{"id":35, "date":date(2024, 1, 1)},
	{"id":36, "date":date(2024, 1, 3)},
	{"id":37, "date":date(2024, 1, 10)},
	{"id":38, "date":date(2024, 1, 19)},
	{"id":39, "date":date(2024, 2, 1)},
	{"id":40, "date":date(2024, 2, 28)},
	{"id":41, "date":date(2024, 1, 22)},
	{"id":42, "date":date(2024, 1, 31)},
	{"id":43, "date":date(2023, 4, 1)},
	{"id":44, "date":date(2024, 2, 14)},
	{"id":45, "date":date(2024, 2, 20)},
]
actions = [
	{"id": 1, "name": "создание пользователя"},
	{"id": 2, "name": "успешный вход"},
	{"id": 3, "name": "выход"},
	{"id": 4, "name": "создание счетчика"},
	{"id": 5, "name": "переименование счетчика"},
	{"id": 6, "name": "удаление счетчика"},
	{"id": 7, "name": "внесение показаний"},
	{"id": 8, "name": "изменение показаний"},
	{"id": 9, "name": "удаление показаний"},
	{"id": 10, "name": "просмотр показаний"},
	{"id": 11, "name": "попытка входа"},

]