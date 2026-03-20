from wtforms.validators import ValidationError

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "mp4", "webm", "ogg"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


from wtforms.validators import ValidationError

def file_size_limit(max_size):
    def _file_size(form, field):

        if not field.data:
            return

        for f in field.data:

            if not f:
                continue

            f.seek(0, 2)
            size = f.tell()
            f.seek(0)

            if size > max_size:
                raise ValidationError(
                    f"{f.filename} exceeds the maximum allowed size of 20MB"
                )

    return _file_size