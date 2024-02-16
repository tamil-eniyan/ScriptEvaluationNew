from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

# class SubjectForm(FlaskForm):
#     subject_id = StringField('Subject ID', validators=[DataRequired()])
#     subject_name = StringField('Name', validators=[DataRequired()])
#     evaluation_scheme = FileField('Evaluation Scheme', validators=[DataRequired()])
#     submit = SubmitField('Add Subject')

# class StudentForm(FlaskForm):
#     roll_number = StringField('Roll Number', validators=[DataRequired()])
#     name = StringField('Name', validators=[DataRequired()])
#     sub_name = StringField('Subject Name', validators=[DataRequired()])
#     answer_script = FileField('Answer Script', validators=[DataRequired()])
#     submit = SubmitField('Add Student')


class EvalForm(FlaskForm):
    exam_type = StringField('Exam Type', validators=[DataRequired()])
    subject_id = StringField('Subject ID', validators=[DataRequired()])
    evaluation_scheme_csv = FileField('Evaluation Schemes', validators=[DataRequired()])
    submit = SubmitField('Add Scheme')

class AnswerScriptForm(FlaskForm):
    exam_type = StringField('Exam Type', validators=[DataRequired()])
    subject_id = StringField('Subject ID', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    answer_script_file = FileField('Answer Script', validators=[DataRequired()])
    submit = SubmitField('Add Answer Script')

