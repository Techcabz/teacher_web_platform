from flask import render_template
from sqlalchemy import func, case
from app.models.file_models import File
from app.models.user_models import User
from app.extensions import db

def report():
    # Construct fullname in the query
    fullname_expr = db.func.concat(
        User.firstname,
        case(
            (User.middlename.isnot(None), ' ' + User.middlename),
            else_=''
        ),
        ' ',
        User.lastname
    )

    # Get users ordered by number of files uploaded (count)
    user_uploads = (
        db.session.query(
            User.id, 
            fullname_expr.label('fullname'),
            func.count(File.id).label('file_count'),
            func.sum(File.file_size).label('total_size')
        )
        .join(File, File.uploader_id == User.id)
        .group_by(User.id, User.firstname, User.middlename, User.lastname)
        .order_by(func.count(File.id).desc())
        .all()
    )

    most_active_user = user_uploads[0] if user_uploads else None

    return render_template(
        'admin/report.html',
        user_uploads=user_uploads,
        most_active_user=most_active_user
    )