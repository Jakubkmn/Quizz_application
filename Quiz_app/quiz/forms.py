from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Quiz, Question, Answer

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'})) 
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'topic', 'number_of_questions')
        widget = {
            'name': forms.TextInput(attrs={'class': 'quiz_name'}),
            'topic': forms.Textarea(attrs={'class': 'quiz_topic'}),
            'number_of_questions': forms.NumberInput(attrs={'class': 'question_num'}),
        }

class QuestionForm(forms.ModelForm):
    choice1_text = forms.CharField(max_length=300, label="", widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice1_correctness = forms.BooleanField(label="", required=False, widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'}))

    choice2_text = forms.CharField(max_length=300, label="", widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice2_correctness = forms.BooleanField(label="", required=False, widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'}))

    choice3_text = forms.CharField(max_length=300, label="", widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice3_correctness = forms.BooleanField(label="", required=False, widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'}))

    choice4_text = forms.CharField(max_length=300, label="", widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice4_correctness = forms.BooleanField(label="", required=False, widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'}))
    class Meta:
        model = Question
        fields = ('question_text',)
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_text', 'correct')
        wigdet = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'correct': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
