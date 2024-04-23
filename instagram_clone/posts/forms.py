from .models import Post, Comment, Feed
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
           
            'content': forms.Textarea(attrs={'class': 'my-class'})
        }
        error_messages = {
            'title': {
                'max_length': '입력 길이를 초과했습니다.'
            }
        }
        
class FeedForm(forms.ModelForm):
    
    class Meta:
        model = Feed
        fields = ['content', 'user', 'image', 'profile_image', 'like_count']
        
        # 모든 필드를 사용
        # fields = '__all__'

        # 지정 필드만 사용
        # fields = ['content']

        # 특정 필드 제외
        # exclude = ['title']

        # fields = ['title', 'content']
        