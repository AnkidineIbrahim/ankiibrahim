"""
Ibrahim Ankidine — Portfolio Flask
app.py : Application principale
"""

import os, json, uuid
from io import BytesIO
from datetime import datetime, timezone
from flask import (Flask, render_template, redirect, url_for,
                   request, flash, jsonify, send_from_directory, abort, send_file)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user,
                         logout_user, login_required, current_user)
from markupsafe import Markup, escape
from sqlalchemy import inspect, text
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ── APP ──────────────────────────────────────────────────────
app = Flask(__name__)

# Use DATABASE_URL from Railway PostgreSQL service
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    # Fix psycopg2 compatibility: postgres:// → postgresql://
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod'),
    SQLALCHEMY_DATABASE_URI=database_url or 'sqlite:///portfolio.db',  # fallback for local dev
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER=os.path.join('static', 'uploads'),
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'webp', 'pdf'},
)

DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'ankidine')
DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'ibrahim123')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Veuillez vous connecter.'

# ── MODELS ───────────────────────────────────────────────────

class Admin(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Profile(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), default='Ibrahim Ankidine')
    title       = db.Column(db.String(200), default='Développeur Web Full Stack')
    bio         = db.Column(db.Text,        default='Passionné par la création d\'applications web modernes.')
    email       = db.Column(db.String(120), default='anki.ib.dev@gmail.com')
    phone       = db.Column(db.String(30),  default='')
    location    = db.Column(db.String(100), default='Moindzaza Mboini, Comores')
    linkedin    = db.Column(db.String(200), default='https://linkedin.com/in/ibrahim-ankidine')
    github      = db.Column(db.String(200), default='https://github.com/AnkidineIbrahim')
    photo       = db.Column(db.String(200), default='images/profile.png')
    cv_file     = db.Column(db.String(200), default='cv_ibrahim_ankidine.pdf')
    available   = db.Column(db.Boolean,     default=True)
    years_exp   = db.Column(db.Integer,     default=3)
    companies   = db.Column(db.Integer,     default=2)
    tech_count  = db.Column(db.Integer,     default=10)
    languages   = db.Column(db.Text,        default='[]')

    def get_languages(self):
        try:
            return json.loads(self.languages or '[]')
        except (TypeError, json.JSONDecodeError):
            return []

class Experience(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    company     = db.Column(db.String(100), nullable=False)
    role        = db.Column(db.String(200), nullable=False)
    period      = db.Column(db.String(80),  nullable=False)
    bullets     = db.Column(db.Text,        default='[]')   # JSON list
    order       = db.Column(db.Integer,     default=0)
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)

    def get_bullets(self):
        return json.loads(self.bullets or '[]')

class Skill(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80),  nullable=False)
    icon     = db.Column(db.String(80),  default='fas fa-code')
    items    = db.Column(db.Text,        default='[]')  # JSON list
    order    = db.Column(db.Integer,     default=0)

    def get_items(self):
        return json.loads(self.items or '[]')

class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    number      = db.Column(db.String(4),   default='01')
    tag         = db.Column(db.String(100), default='Web App')
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False)
    tech        = db.Column(db.Text,        default='[]')  # JSON list
    github_url  = db.Column(db.String(300), default='#')
    live_url    = db.Column(db.String(300), default='#')
    order       = db.Column(db.Integer,     default=0)
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)

    def get_tech(self):
        return json.loads(self.tech or '[]')

class Education(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    degree  = db.Column(db.String(200), nullable=False)
    school  = db.Column(db.String(200), nullable=False)
    period  = db.Column(db.String(80),  nullable=False)
    icon    = db.Column(db.String(80),  default='fas fa-university')
    order   = db.Column(db.Integer,     default=0)

class Message(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    content    = db.Column(db.Text,        nullable=False)
    read       = db.Column(db.Boolean,     default=False)
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)

class Visit(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    page       = db.Column(db.String(80),  default='home')
    ip         = db.Column(db.String(60),  default='')
    user_agent = db.Column(db.String(300), default='')
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)


def ensure_schema_updates():
    inspector = inspect(db.engine)

    if inspector.has_table('profile'):
        profile_columns = {column['name'] for column in inspector.get_columns('profile')}
        if 'languages' not in profile_columns:
            db.session.execute(text("ALTER TABLE profile ADD COLUMN languages TEXT DEFAULT '[]'"))
            db.session.commit()


with app.app_context():
    db.create_all()
    ensure_schema_updates()

# ── HELPERS ──────────────────────────────────────────────────

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_upload(file, folder='uploads'):
    if file and allowed_file(file.filename):
        ext  = file.filename.rsplit('.', 1)[1].lower()
        name = secure_filename(f"{uuid.uuid4().hex}.{ext}")
        path = os.path.join('static', folder, name)
        file.save(path)
        return f"{folder}/{name}"
    return None

def record_visit(page='home'):
    try:
        v = Visit(page=page,
                  ip=request.remote_addr or '',
                  user_agent=request.user_agent.string[:300])
        db.session.add(v); db.session.commit()
    except Exception:
        pass

def build_cv_pdf(profile, experiences, skills, projects, education):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.45 * cm,
        rightMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm,
        title=f"CV {profile.name}",
        author=profile.name,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CvName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=27,
        textColor=colors.white,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='CvTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#F6DFA4'),
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='CvSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#111827'),
        backColor=colors.HexColor('#F8F4EA'),
        borderPadding=(5, 7, 5, 7),
        spaceBefore=0,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='CvBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
    ))
    styles.add(ParagraphStyle(
        name='CvMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.7,
        leading=11.5,
        textColor=colors.HexColor('#4B5563'),
    ))
    styles.add(ParagraphStyle(
        name='CvRight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#374151'),
    ))
    styles.add(ParagraphStyle(
        name='CvMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.3,
        leading=10,
        textColor=colors.HexColor('#A16207'),
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='CvSidebarSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=11,
        textColor=colors.white,
        backColor=colors.HexColor('#B2872F'),
        borderPadding=(5, 7, 5, 7),
        spaceBefore=0,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='CvSidebarBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.7,
        leading=11.4,
        textColor=colors.HexColor('#E5E7EB'),
    ))
    styles.add(ParagraphStyle(
        name='CvSidebarMuted',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.1,
        leading=10.2,
        textColor=colors.HexColor('#F6DFA4'),
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='CvSmall',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.4,
        leading=10.8,
        textColor=colors.HexColor('#4B5563'),
    ))

    def clean_lines(value):
        return '<br/>'.join(
            escape(line.strip())
            for line in (value or '').splitlines()
            if line.strip()
        )

    def list_to_sentence(items):
        return ', '.join(escape(item) for item in items if item)

    def get_profile_image():
        photo = (profile.photo or '').strip()
        if not photo:
            return None

        image_path = os.path.join(app.root_path, 'static', photo.replace('/', os.sep))
        if not os.path.exists(image_path):
            return None

        avatar = Image(image_path, width=2.55 * cm, height=2.55 * cm)
        avatar.hAlign = 'LEFT'
        return avatar

    story = []
    accent = colors.HexColor('#C89B3C')
    dark = colors.HexColor('#111827')
    light = colors.HexColor('#F8FAFC')
    border = colors.HexColor('#E5E7EB')

    identity_block = [
        Paragraph(escape(profile.name), styles['CvName']),
        Paragraph(escape(profile.title or ''), styles['CvTitle']),
    ]

    profile_image = get_profile_image()
    if profile_image:
        header_left = Table(
            [[profile_image, identity_block]],
            colWidths=[2.95 * cm, 7.4 * cm]
        )
        header_left.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
    else:
        header_left = identity_block

    header_right = []
    if profile.email:
        header_right.append(Paragraph(escape(profile.email), styles['CvSidebarBody']))
    if profile.phone:
        header_right.append(Paragraph(escape(profile.phone), styles['CvSidebarBody']))
    if profile.location:
        header_right.append(Paragraph(escape(profile.location), styles['CvSidebarBody']))
    if profile.linkedin:
        header_right.append(Paragraph(escape(profile.linkedin), styles['CvSidebarBody']))
    if profile.github:
        header_right.append(Paragraph(escape(profile.github), styles['CvSidebarBody']))

    header = Table(
        [[header_left, header_right]],
        colWidths=[10.9 * cm, 5.8 * cm]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), dark),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(header)
    story.append(Spacer(1, 0.34 * cm))

    left_column = []
    right_column = []

    left_column.append(Paragraph('Profil', styles['CvSidebarSection']))
    availability_text = (
        'Disponible pour de nouvelles missions'
        if profile.available else
        'Actuellement occupe'
    )
    left_column.append(Paragraph(availability_text, styles['CvSidebarBody']))
    if profile.bio:
        left_column.append(Spacer(1, 0.14 * cm))
        left_column.append(Paragraph(clean_lines(profile.bio), styles['CvSidebarBody']))

    if skills:
        left_column.append(Spacer(1, 0.18 * cm))
        left_column.append(Paragraph('Competences', styles['CvSidebarSection']))
        for skill in skills:
            items = list_to_sentence(skill.get_items())
            if items:
                left_column.append(Paragraph(escape(skill.category).upper(), styles['CvSidebarMuted']))
                left_column.append(Paragraph(items, styles['CvSidebarBody']))
                left_column.append(Spacer(1, 0.12 * cm))

    right_column.append(Paragraph('Experience professionnelle', styles['CvSection']))
    if experiences:
        for exp in experiences:
            left = Paragraph(
                f"<b>{escape(exp.role)}</b><br/>{escape(exp.company)}",
                styles['CvBody']
            )
            right = Paragraph(escape(exp.period), styles['CvRight'])
            exp_table = Table([[left, right]], colWidths=[8.7 * cm, 3.2 * cm])
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LINEBELOW', (0, 0), (-1, 0), 0.4, border),
            ]))
            right_column.append(exp_table)
            for bullet in exp.get_bullets():
                right_column.append(Paragraph(f"- {escape(bullet)}", styles['CvBody']))
            right_column.append(Spacer(1, 0.16 * cm))
    else:
        right_column.append(Paragraph("Aucune experience renseignee pour le moment.", styles['CvSmall']))

    if education:
        right_column.append(Spacer(1, 0.12 * cm))
        right_column.append(Paragraph('Formation', styles['CvSection']))
        for edu in education:
            left = Paragraph(
                f"<b>{escape(edu.degree)}</b><br/>{escape(edu.school)}",
                styles['CvBody']
            )
            right = Paragraph(escape(edu.period), styles['CvRight'])
            row = Table([[left, right]], colWidths=[8.7 * cm, 3.2 * cm])
            row.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LINEBELOW', (0, 0), (-1, 0), 0.35, border),
            ]))
            right_column.append(row)

    body = Table(
        [[left_column, right_column]],
        colWidths=[5.0 * cm, 10.9 * cm]
    )
    body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), dark),
        ('BACKGROUND', (1, 0), (1, 0), light),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 13),
        ('RIGHTPADDING', (0, 0), (0, 0), 13),
        ('TOPPADDING', (0, 0), (0, 0), 16),
        ('BOTTOMPADDING', (0, 0), (0, 0), 16),
        ('LEFTPADDING', (1, 0), (1, 0), 16),
        ('RIGHTPADDING', (1, 0), (1, 0), 16),
        ('TOPPADDING', (1, 0), (1, 0), 16),
        ('BOTTOMPADDING', (1, 0), (1, 0), 16),
        ('LINEABOVE', (1, 0), (1, 0), 4, accent),
        ('BOX', (0, 0), (-1, -1), 0.6, border),
    ]))
    story.append(body)

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.template_filter('nl2br')
def nl2br_filter(value):
    text = escape((value or '').replace('\r\n', '\n'))
    return Markup(str(text).replace('\n', '<br>\n'))

@app.template_filter('paragraphs')
def paragraphs_filter(value):
    text = (value or '').replace('\r\n', '\n').strip()
    if not text:
        return Markup('')

    blocks = [block.strip() for block in text.split('\n\n') if block.strip()]
    html = []
    for block in blocks:
        escaped = escape(block)
        html.append(f'<p>{str(escaped).replace(chr(10), "<br>")}</p>')
    return Markup(''.join(html))

# ── PUBLIC ROUTES ─────────────────────────────────────────────

@app.route('/')
def index():
    record_visit('home')
    profile     = Profile.query.first()
    experiences = Experience.query.order_by(Experience.order).all()
    skills      = Skill.query.order_by(Skill.order).all()
    projects    = Project.query.order_by(Project.order).all()
    education   = Education.query.order_by(Education.order).all()
    return render_template('public/index.html',
                           profile=profile,
                           experiences=experiences,
                           skills=skills,
                           projects=projects,
                           education=education)

@app.route('/contact', methods=['POST'])
def contact():
    payload = request.get_json(silent=True) or request.form
    name    = (payload.get('name') or '').strip()
    email   = (payload.get('email') or '').strip()
    content = (payload.get('message') or '').strip()
    if not (name and email and content):
        return jsonify({'ok': False, 'error': 'Champs manquants'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'ok': False, 'error': 'Adresse email invalide'}), 400
    msg = Message(name=name, email=email, content=content)
    db.session.add(msg); db.session.commit()
    return jsonify({'ok': True})

@app.route('/download-cv')
def download_cv():
    record_visit('cv_download')
    profile = Profile.query.first()
    if not profile:
        return abort(404)

    experiences = Experience.query.order_by(Experience.order).all()
    skills = Skill.query.order_by(Skill.order).all()
    projects = Project.query.order_by(Project.order).all()
    education = Education.query.order_by(Education.order).all()

    pdf = build_cv_pdf(profile, experiences, skills, projects, education)
    safe_name = secure_filename(profile.name.replace(' ', '_')) or 'CV'
    return send_file(
        pdf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"CV_{safe_name}.pdf",
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.svg', mimetype='image/svg+xml'
    )

# ── ADMIN AUTH ────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        u = Admin.query.filter_by(username=request.form.get('username')).first()
        if u and check_password_hash(u.password, request.form.get('password', '')):
            login_user(u)
            return redirect(url_for('admin_dashboard'))
        flash('Identifiants incorrects.', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

# ── ADMIN DASHBOARD ───────────────────────────────────────────

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'visits_total'  : Visit.query.count(),
        'visits_today'  : Visit.query.filter(
                            Visit.created_at >= datetime.now(timezone.utc).date()).count(),
        'messages_total': Message.query.count(),
        'messages_unread': Message.query.filter_by(read=False).count(),
        'projects'      : Project.query.count(),
        'experiences'   : Experience.query.count(),
    }
    recent_msgs = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    # Visites par page
    pages = db.session.query(Visit.page, db.func.count(Visit.id))\
                      .group_by(Visit.page).all()
    return render_template('admin/dashboard.html',
                           stats=stats, recent_msgs=recent_msgs, pages=pages)

# ── ADMIN PROFILE ─────────────────────────────────────────────

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    p = Profile.query.first()
    if request.method == 'POST':
        p.name       = request.form.get('name', p.name)
        p.title      = request.form.get('title', p.title)
        p.bio        = request.form.get('bio', p.bio)
        p.email      = request.form.get('email', p.email)
        p.phone      = request.form.get('phone', p.phone)
        p.location   = request.form.get('location', p.location)
        p.linkedin   = request.form.get('linkedin', p.linkedin)
        p.github     = request.form.get('github', p.github)
        # The form sends a hidden "0" plus the checkbox "1" when checked.
        # Use getlist() so the checked state wins whenever "1" is present.
        p.available  = '1' in request.form.getlist('available')
        p.years_exp  = int(request.form.get('years_exp', p.years_exp) or 0)
        p.companies  = int(request.form.get('companies',  p.companies) or 0)
        p.tech_count = int(request.form.get('tech_count', p.tech_count) or 0)
        raw_languages = request.form.get('languages', '')
        languages = [
            item.strip()
            for item in raw_languages.replace('\r', '').replace('\n', ',').split(',')
            if item.strip()
        ]
        p.languages  = json.dumps(languages, ensure_ascii=False)
        # Photo upload
        photo = request.files.get('photo')
        if photo and photo.filename:
            path = save_upload(photo)
            if path: p.photo = path
        # CV upload
        cv = request.files.get('cv')
        if cv and cv.filename:
            path = save_upload(cv)
            if path: p.cv_file = path
        db.session.commit()
        flash('Profil mis à jour !', 'success')
        return redirect(url_for('admin_profile'))
    return render_template('admin/profile.html', profile=p)

# ── ADMIN PROJECTS ────────────────────────────────────────────

@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.order).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@login_required
def admin_project_new():
    if request.method == 'POST':
        tech = [t.strip() for t in request.form.get('tech','').split(',') if t.strip()]
        p = Project(
            number      = request.form.get('number', '01'),
            tag         = request.form.get('tag', ''),
            title       = request.form.get('title', ''),
            description = request.form.get('description', ''),
            tech        = json.dumps(tech),
            github_url  = request.form.get('github_url', '#'),
            live_url    = request.form.get('live_url', '#'),
            order       = int(request.form.get('order', 0) or 0),
        )
        db.session.add(p); db.session.commit()
        flash('Projet ajouté !', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/project_form.html', project=None)

@app.route('/admin/projects/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def admin_project_edit(pid):
    p = db.session.get(Project, pid) or abort(404)
    if request.method == 'POST':
        tech = [t.strip() for t in request.form.get('tech','').split(',') if t.strip()]
        p.number      = request.form.get('number', p.number)
        p.tag         = request.form.get('tag', p.tag)
        p.title       = request.form.get('title', p.title)
        p.description = request.form.get('description', p.description)
        p.tech        = json.dumps(tech)
        p.github_url  = request.form.get('github_url', p.github_url)
        p.live_url    = request.form.get('live_url', p.live_url)
        p.order       = int(request.form.get('order', p.order) or 0)
        db.session.commit()
        flash('Projet mis à jour !', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/project_form.html', project=p)

@app.route('/admin/projects/<int:pid>/delete', methods=['POST'])
@login_required
def admin_project_delete(pid):
    p = db.session.get(Project, pid) or abort(404)
    db.session.delete(p)
    db.session.commit()
    flash('Projet supprimé.', 'info')
    return redirect(url_for('admin_projects'))

# ── ADMIN EXPERIENCES ─────────────────────────────────────────

@app.route('/admin/experiences')
@login_required
def admin_experiences():
    exps = Experience.query.order_by(Experience.order).all()
    return render_template('admin/experiences.html', experiences=exps)

@app.route('/admin/experiences/new', methods=['GET', 'POST'])
@login_required
def admin_experience_new():
    if request.method == 'POST':
        bullets_raw = request.form.get('bullets', '')
        bullets = [b.strip() for b in bullets_raw.split('\n') if b.strip()]
        e = Experience(
            company = request.form.get('company', ''),
            role    = request.form.get('role', ''),
            period  = request.form.get('period', ''),
            bullets = json.dumps(bullets),
            order   = int(request.form.get('order', 0) or 0),
        )
        db.session.add(e); db.session.commit()
        flash('Expérience ajoutée !', 'success')
        return redirect(url_for('admin_experiences'))
    return render_template('admin/experience_form.html', exp=None)

@app.route('/admin/experiences/<int:eid>/edit', methods=['GET', 'POST'])
@login_required
def admin_experience_edit(eid):
    e = db.session.get(Experience, eid) or abort(404)
    if request.method == 'POST':
        bullets_raw = request.form.get('bullets', '')
        bullets = [b.strip() for b in bullets_raw.split('\n') if b.strip()]
        e.company = request.form.get('company', e.company)
        e.role    = request.form.get('role',    e.role)
        e.period  = request.form.get('period',  e.period)
        e.bullets = json.dumps(bullets)
        e.order   = int(request.form.get('order', e.order) or 0)
        db.session.commit()
        flash('Expérience mise à jour !', 'success')
        return redirect(url_for('admin_experiences'))
    return render_template('admin/experience_form.html', exp=e)

@app.route('/admin/experiences/<int:eid>/delete', methods=['POST'])
@login_required
def admin_experience_delete(eid):
    e = db.session.get(Experience, eid) or abort(404)
    db.session.delete(e)
    db.session.commit()
    flash('Expérience supprimée.', 'info')
    return redirect(url_for('admin_experiences'))

# ── ADMIN SKILLS ──────────────────────────────────────────────

@app.route('/admin/skills')
@login_required
def admin_skills():
    skills = Skill.query.order_by(Skill.order).all()
    return render_template('admin/skills.html', skills=skills)

@app.route('/admin/skills/new', methods=['GET', 'POST'])
@login_required
def admin_skill_new():
    if request.method == 'POST':
        items = [i.strip() for i in request.form.get('items','').split(',') if i.strip()]
        s = Skill(
            category = request.form.get('category',''),
            icon     = request.form.get('icon','fas fa-code'),
            items    = json.dumps(items),
            order    = int(request.form.get('order',0) or 0),
        )
        db.session.add(s); db.session.commit()
        flash('Compétence ajoutée !', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/skill_form.html', skill=None)

@app.route('/admin/skills/<int:sid>/edit', methods=['GET', 'POST'])
@login_required
def admin_skill_edit(sid):
    s = db.session.get(Skill, sid) or abort(404)
    if request.method == 'POST':
        items = [i.strip() for i in request.form.get('items','').split(',') if i.strip()]
        s.category = request.form.get('category', s.category)
        s.icon     = request.form.get('icon',     s.icon)
        s.items    = json.dumps(items)
        s.order    = int(request.form.get('order', s.order) or 0)
        db.session.commit()
        flash('Compétence mise à jour !', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/skill_form.html', skill=s)

@app.route('/admin/skills/<int:sid>/delete', methods=['POST'])
@login_required
def admin_skill_delete(sid):
    s = db.session.get(Skill, sid) or abort(404)
    db.session.delete(s)
    db.session.commit()
    flash('Compétence supprimée.', 'info')
    return redirect(url_for('admin_skills'))

# ── ADMIN EDUCATION ───────────────────────────────────────────

@app.route('/admin/education')
@login_required
def admin_education():
    edus = Education.query.order_by(Education.order).all()
    return render_template('admin/education.html', educations=edus)

@app.route('/admin/education/new', methods=['GET', 'POST'])
@login_required
def admin_education_new():
    if request.method == 'POST':
        e = Education(
            degree = request.form.get('degree',''),
            school = request.form.get('school',''),
            period = request.form.get('period',''),
            icon   = request.form.get('icon','fas fa-university'),
            order  = int(request.form.get('order',0) or 0),
        )
        db.session.add(e); db.session.commit()
        flash('Formation ajoutée !', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', edu=None)

@app.route('/admin/education/<int:eid>/edit', methods=['GET', 'POST'])
@login_required
def admin_education_edit(eid):
    e = db.session.get(Education, eid) or abort(404)
    if request.method == 'POST':
        e.degree = request.form.get('degree', e.degree)
        e.school = request.form.get('school', e.school)
        e.period = request.form.get('period', e.period)
        e.icon   = request.form.get('icon',   e.icon)
        e.order  = int(request.form.get('order', e.order) or 0)
        db.session.commit()
        flash('Formation mise à jour !', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', edu=e)

@app.route('/admin/education/<int:eid>/delete', methods=['POST'])
@login_required
def admin_education_delete(eid):
    e = db.session.get(Education, eid) or abort(404)
    db.session.delete(e)
    db.session.commit()
    flash('Formation supprimée.', 'info')
    return redirect(url_for('admin_education'))

# ── ADMIN MESSAGES ────────────────────────────────────────────

@app.route('/admin/messages')
@login_required
def admin_messages():
    msgs = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=msgs)

@app.route('/admin/messages/<int:mid>/read', methods=['POST'])
@login_required
def admin_message_read(mid):
    m = db.session.get(Message, mid) or abort(404)
    m.read = True; db.session.commit()
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/<int:mid>/delete', methods=['POST'])
@login_required
def admin_message_delete(mid):
    m = db.session.get(Message, mid) or abort(404)
    db.session.delete(m)
    db.session.commit()
    flash('Message supprimé.', 'info')
    return redirect(url_for('admin_messages'))

# ── ADMIN STATS ───────────────────────────────────────────────

@app.route('/admin/stats')
@login_required
def admin_stats():
    from sqlalchemy import func, text

    daily_raw = db.session.execute(
        text("""
            SELECT DATE(created_at) as day,
                   COUNT(*) as count
            FROM visit
            GROUP BY DATE(created_at)
            ORDER BY day DESC
            LIMIT 30
        """)
    ).fetchall()
    # Convertir en listes simples pour un rendu Jinja/JS fiable.
    daily = [
        {
            'day': str(day),
            'count': int(count or 0),
        }
        for day, count in reversed(daily_raw)
    ]

    pages_raw = db.session.query(
        Visit.page, func.count(Visit.id).label('count')
    ).group_by(Visit.page).order_by(func.count(Visit.id).desc()).all()

    pages = [
        {
            'page': page or 'home',
            'count': int(count or 0),
        }
        for page, count in pages_raw
    ]

    return render_template('admin/stats.html', daily=daily, pages=pages,
                           total=Visit.query.count())

# ── INIT DB ───────────────────────────────────────────────────

def init_db(reset_admin=False):
    with app.app_context():
        db.create_all()
        ensure_schema_updates()

        # Admin par défaut
        admin = Admin.query.first()
        if not admin:
            db.session.add(Admin(
                username=DEFAULT_ADMIN_USERNAME,
                password=generate_password_hash(DEFAULT_ADMIN_PASSWORD)
            ))
        elif reset_admin:
            admin.username = DEFAULT_ADMIN_USERNAME
            admin.password = generate_password_hash(DEFAULT_ADMIN_PASSWORD)

        # Profil par défaut
        if not Profile.query.first():
            db.session.add(Profile(languages=json.dumps(['Français', 'Anglais', 'Comorien'], ensure_ascii=False)))

        # Expériences
        if not Experience.query.first():
            exps = [
                Experience(
                    company='ANAMEV', role='Développeur Web Full Stack',
                    period='2022 — Présent',
                    bullets=json.dumps([
                        'Développement et maintenance d\'applications web internes',
                        'Intégration de systèmes de gestion d\'actifs (Snipe-IT)',
                        'Création et documentation d\'APIs RESTful avec Laravel',
                        'Personnalisation avancée de dashboards et interfaces admin',
                    ]), order=0
                ),
                Experience(
                    company='ALLA Voyage', role='Responsable développement plateforme',
                    period='Expérience précédente',
                    bullets=json.dumps([
                        'Conception et développement de la plateforme web de l\'agence',
                        'Gestion complète de l\'infrastructure applicative',
                        'Optimisation des performances et de l\'expérience utilisateur',
                    ]), order=1
                ),
            ]
            db.session.add_all(exps)

        # Compétences
        if not Skill.query.first():
            skills = [
                Skill(category='Langages', icon='fas fa-code',
                      items=json.dumps(['PHP','JavaScript','HTML5','CSS3','SQL','TypeScript']), order=0),
                Skill(category='Frameworks', icon='fas fa-layer-group',
                      items=json.dumps(['Laravel','React','Vue.js','Blade','Tailwind CSS','Bootstrap']), order=1),
                Skill(category='Outils', icon='fas fa-tools',
                      items=json.dumps(['Git','Docker','VS Code','Figma']), order=2),
                Skill(category='Bases de données', icon='fas fa-database',
                      items=json.dumps(['MySQL','PostgreSQL','SQLite']), order=3),
            ]
            db.session.add_all(skills)

        # Projets
        if not Project.query.first():
            projects = [
                Project(number='01', tag='Web App · Éducation', title='Quiz Champion',
                        description='Application de quiz interactive avec timer dynamique, système de scoring progressif et animations fluides.',
                        tech=json.dumps(['HTML5','CSS3','JavaScript','Animations']),
                        github_url='https://github.com/AnkidineIbrahim', order=0),
                Project(number='02', tag='Dashboard · Laravel', title='Dashboard Personnalisé',
                        description='Refonte complète d\'un tableau de bord de gestion d\'actifs (Snipe-IT). Nouveau layout CSS Flexbox et composants modernes Blade.',
                        tech=json.dumps(['Laravel','Blade','PHP','CSS3']),
                        github_url='https://github.com/AnkidineIbrahim', order=1),
                Project(number='03', tag='Plateforme · Voyage', title='Plateforme ALLA Voyage',
                        description='Développement complet d\'une plateforme web pour une agence de voyage avec gestion des réservations et espace clients.',
                        tech=json.dumps(['PHP','Laravel','MySQL','JavaScript']),
                        github_url='https://github.com/AnkidineIbrahim', order=2),
            ]
            db.session.add_all(projects)

        # Formation
        if not Education.query.first():
            edus = [
                Education(degree='Licence en Informatique',
                          school='Faculté des Sciences de Fès',
                          period='2018 — 2021', icon='fas fa-university', order=0),
                Education(degree='Baccalauréat TC',
                          school='Les Elites',
                          period='2017', icon='fas fa-school', order=1),
            ]
            db.session.add_all(edus)

        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
