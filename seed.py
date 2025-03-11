from asrp import create_app
from asrp.extensions import db
from asrp.models import User, Unit, Area, Report, Attachment, Content, UserArea, LeakedInfo
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Tạo đơn vị
    unit1 = Unit(name='Đội phòng chống tội phạm mạng', description='Xử lý tội phạm mạng.')
    unit2 = Unit(name='Đội chống gian lận tài chính', description='Xử lý gian lận tài chính.')
    db.session.add_all([unit1, unit2])
    db.session.commit()

    # Tạo user admin
    admin = User(
        full_name='Quản trị viên',
        email='admin@example.com',
        phone_number='0123456789',
        role='admin',
        is_active=True,
        verification_status='verified'
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # Tạo cảnh sát
    po1 = User(
        full_name='Cảnh sát 1',
        email='cs1@example.com',
        phone_number='0111111111',
        role='police_officer',
        unit_id=unit1.id,
        is_active=True,
        verification_status='verified'
    )
    po1.set_password('cs123')

    po2 = User(
        full_name='Cảnh sát 2',
        email='cs2@example.com',
        phone_number='0222222222',
        role='police_officer',
        unit_id=unit2.id,
        is_active=True,
        verification_status='verified'
    )
    po2.set_password('cs123')
    db.session.add_all([po1, po2])

    # Tạo user thường
    user1 = User(
        full_name='Người dùng 1',
        email='nd1@example.com',
        phone_number='0333333333',
        role='user',
        is_active=True,
        verification_status='verified'
    )
    user1.set_password('nd123')

    user2 = User(
        full_name='Người dùng 2',
        email='nd2@example.com',
        phone_number='0444444444',
        role='user',
        is_active=True,
        verification_status='verified'
    )
    user2.set_password('nd123')
    db.session.add_all([user1, user2])
    db.session.commit()

    # Tạo khu vực
    # Bỏ quận 1 và quận 2, thêm các khu vực tương ứng với Bắc Ninh
    # Thêm tỉnh Bắc Ninh và các huyện
    area1 = Area(name='Thành phố Bắc Ninh', description='Thành phố Bắc Ninh.')
    area2 = Area(name='Huyện Gia Bình', description='Huyện Gia Bình, Bắc Ninh.')
    area3 = Area(name='Huyện Lương Tài', description='Huyện Lương Tài, Bắc Ninh.')
    area4 = Area(name='Huyện Quế Võ', description='Huyện Quế Võ, Bắc Ninh.')
    area5 = Area(name='Huyện Tiên Du', description='Huyện Tiên Du, Bắc Ninh.')
    area6 = Area(name='Huyện Yên Phong', description='Huyện Yên Phong, Bắc Ninh.')
    area7 = Area(name='Huyện Thuận Thành', description='Huyện Thuận Thành, Bắc Ninh.')
    area8 = Area(name='Huyện Từ Sơn', description='Huyện Từ Sơn, Bắc Ninh.')
    area9 = Area(name='Huyện Bắc Ninh', description='Huyện Bắc Ninh.')

    db.session.add_all([area1, area2, area3, area4, area5, area6, area7, area8, area9])
    db.session.commit()

    # Gán cảnh sát vào khu vực
    ua1 = UserArea(user_id=po1.id, area_id=area1.id)
    ua2 = UserArea(user_id=po2.id, area_id=area2.id)
    db.session.add_all([ua1, ua2])
    db.session.commit()

    # Tạo vài báo cáo
    for i in range(1, 6):
        r = Report(
            user_id=random.choice([user1.id, user2.id]),
            area_id=random.choice([area1.id, area2.id]),
            title=f'Lừa đảo {i}',
            description=f'Chi tiết vụ lừa đảo {i}',
            latitude=random.uniform(10.0, 20.0),  # Example latitude
            longitude=random.uniform(100.0, 110.0),  # Example longitude
            status='new',  # Initial status
            assigned_officer_id=random.choice([po1.id, po2.id])  # Randomly assign an officer
        )
        db.session.add(r)
    db.session.commit()

    # Tạo vài nội dung
    content1 = Content(
        title='Cách phòng tránh lừa đảo trực tuyến',
        body='Nội dung chi tiết về cách phòng tránh...',
        author_id=admin.id
    )
    content2 = Content(
        title='Cảnh báo lừa đảo mới nhất',
        body='Thông tin cảnh báo...',
        author_id=admin.id
    )
    db.session.add_all([content1, content2])
    db.session.commit()

    # Thêm dữ liệu seed cho LeakedInfo
    leaked_infos = [
        LeakedInfo(contact_info='leaked1@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked2@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked3@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked4@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked5@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked6@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked7@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked8@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked9@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked10@example.com', info_type='email'),
        LeakedInfo(contact_info='0123456789', info_type='phone'),
        LeakedInfo(contact_info='0987654321', info_type='phone'),
        LeakedInfo(contact_info='0912345678', info_type='phone'),
        LeakedInfo(contact_info='0908765432', info_type='phone'),
        LeakedInfo(contact_info='0934567890', info_type='phone'),
        LeakedInfo(contact_info='0945678901', info_type='phone'),
        LeakedInfo(contact_info='0956789012', info_type='phone'),
        LeakedInfo(contact_info='0967890123', info_type='phone'),
        LeakedInfo(contact_info='0978901234', info_type='phone'),
        LeakedInfo(contact_info='0989012345', info_type='phone'),
        LeakedInfo(contact_info='leaked11@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked12@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked13@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked14@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked15@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked16@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked17@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked18@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked19@example.com', info_type='email'),
        LeakedInfo(contact_info='leaked20@example.com', info_type='email'),
    ]

    db.session.add_all(leaked_infos)
    db.session.commit()

    print("Dữ liệu mẫu đã được tạo thành công!")
