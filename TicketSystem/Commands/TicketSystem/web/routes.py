import flask
import os
from extensions import turbo
from ruamel.yaml import YAML
import sqlite3
import re
from markupsafe import Markup, escape


def get_sidebar_item():
    return {
        "label": "Tickets",
        "url": "/TicketSystem",
        "icon": "fas fa-ticket-alt"
    }

blueprint = flask.Blueprint("TicketSystem", __name__)
CONFIG_PATH = os.path.join("Bot", "Configs", "TicketSystem.yml")

yaml = YAML()
yaml.preserve_quotes = True

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.load(f) or {}
    return {}

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f)

@blueprint.route("/settings", methods=["GET", "POST"])
def settings():
    if not ('otp_verified' in flask.session and flask.session['otp_verified']):
        return flask.redirect(flask.url_for('login'))
    config = load_config()
    if flask.request.method == "POST":
        if "toggle_only" in flask.request.form:
            config["enable_categories"] = flask.request.form.get("enable_categories") == "on"
            if not config["enable_categories"]:
                turbo.push(turbo.replace(f'<input type="text" class="form-control" id="ticketCategory" name="ticket_category_id" value="{config["ticket_system"]["ticket_category_id"] if config["ticket_system"]["ticket_category_id"] is not None else ""}" placeholder="Place category id here" wfd-id="id1">', target="ticketCategory"))
                return {"success": True}
            else:
                turbo.push(turbo.replace('<input type="text" class="form-control" id="ticketCategory" name="ticket_category_id" value="" placeholder="Disable categories to use this setting" wfd-id="id1" disabled="">', target="ticketCategory"))
                categories_string_html: str = '<div id="categoriesContainer" bis_skin_checked="1">'
                if config["ticket_system"]["categories"]:
                    for category_name, categories_id in config["ticket_system"]["categories"].items():
                        categories_string_html += f'''<div class="row g-2 mb-2 align-items-center category-row" bis_skin_checked="1">
        <div class="col-md-5" bis_skin_checked="1">
            <input type="text" class="form-control" name="categories_name[]" placeholder="Enable categories to use this setting" value="{category_name}" wfd-id="id2">
        </div>
        <div class="col-md-5" bis_skin_checked="1">
            <input type="text" class="form-control" name="categories_id[]" placeholder="Enable categories to use this setting" value="{categories_id}" wfd-id="id3">
        </div>
        <div class="col-md-2 text-end left" bis_skin_checked="1">
            <button type="button" class="btn btn-sm btn-danger remove-category">×</button>
        </div>
    </div>'''
                turbo.push(turbo.replace(categories_string_html + "</div>", target="categoriesContainer"))
            return {"success": True}

        enable_categories = flask.request.form.get("enable_categories") == "on"
        list_for_values_of_multidict = []
        categories_id = flask.request.form.getlist("categories_id[]")
        categories_name = flask.request.form.getlist("categories_name[]")
        categories = {}
        if (categories_id and categories_name) and len(categories_id) == len(categories_name):
            for i in range(len(categories_id)):
                categories[categories_name[i]] = categories_id[i]

        config = {
            "enable_categories": enable_categories,
            "categories": categories if enable_categories else None,
            "ticket_category_id": None if enable_categories else flask.request.form.get("ticket_category_id"),
            "support_roles": [r for r in flask.request.form.getlist("support_roles[]")],
            "ticket_panel_channel_id": flask.request.form.get("ticket_panel_channel_id"),
            "ticket_log_channel_id": flask.request.form.get("ticket_log_channel_id"),
            "require_staff_approval_for_add_user": flask.request.form.get("require_staff_approval") == "on",
            "ticket_panel_message_id": flask.request.form.get("ticket_panel_message_id"),
        }
        save_config({"ticket_system": config})
        html_message = """<div class="alert alert-info fade show d-flex align-items-center" role="alert" id="info-warning">
<i class="fa fa-check-circle-o me-2"></i>
<span>Your config saved🎉!</span>
<button type="button" class="btn-close ms-auto" aria-label="Close" onclick="hideWarning()" style="border: none; margin: 0;"></button>
</div>"""
        turbo.push(turbo.prepend(html_message, target='main-card'))

        return '', 204

    if flask.request.args.get('reload') is None:
        return flask.render_template('wating.html')

    config = load_config().get("ticket_system", {})
    return flask.render_template("TicketSystem/settings.html", config=config)

@blueprint.route("/transcript/<channel_id>")
#TODO: brs between each day,
def test(channel_id):
    if not ('otp_verified' in flask.session and flask.session['otp_verified']):
        return flask.redirect(flask.url_for('login'))
    conn = sqlite3.connect("Bot/data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM ticketMessages WHERE channel_id = {channel_id} ORDER BY timestamp ASC").fetchall()
    row_dict = []
    for row in rows:
        row_dict.append({
            "message_id": row[1],
            "channel_id": row[2],
            "author_id": row[3],
            "author_name": row[4],
            "author_image": row[5],
            "content": row[6],
            "embed_title": row[7],
            "embed_color": row[8],
            "embed_description": row[9],
            "embed_fields": row[10],
            "embed_image_url": row[11],
            "embed_thumbnail_url": row[12],
            "embed_footer": row[13],
            "embed_icon_url": row[14],
            "embed_icon_text": row[15],
            "timestamp": row[16]
        })
    conn.close()
    return flask.render_template("TicketSystem/transcript.html", rows=row_dict)

@blueprint.route("/")
def index():
    if not ('otp_verified' in flask.session and flask.session['otp_verified']):
        return flask.redirect(flask.url_for('login'))
    conn = sqlite3.connect("Bot/data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    tickets = cur.execute("SELECT * FROM ticketsTicketSystem ORDER BY close_time ASC").fetchall()
    conn.close()
    return flask.render_template("TicketSystem/logs.html", tickets=tickets)

def discord_format(text):
    text = escape(text)  # Prevent XSS

    # Code blocks
    text = re.sub(r"```(.*?)```", r"<pre>\1</pre>", text, flags=re.DOTALL)
    text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)

    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Italics
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    text = re.sub(r"__(.*?)__", r"<em>\1</em>", text)

    # Underline
    text = re.sub(r"__([^_]+)__", r"<u>\1</u>", text)

    # Strikethrough
    text = re.sub(r"~~(.*?)~~", r"<del>\1</del>", text)

    return Markup(text)

blueprint.add_app_template_filter(discord_format, name='discord_format')