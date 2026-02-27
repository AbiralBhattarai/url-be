from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from .models import ShortURL, Click
from .utils.services import generate_short_url,get_clicks_for_url
from .utils.throttle import check_rate_limit
from .serializers import ShortURLSerializer, ClickSerializer
from rest_framework.pagination import PageNumberPagination
import os
from dotenv import load_dotenv
# Create your views here.

load_dotenv()

class CreateShortURLView(APIView):
    def post(self, request):
        try:
            #check rate limit
            allowed, wait_time = check_rate_limit(request)
            if not allowed:
                return Response(
                    {'error': 'Rate limit exceeded', 'retry_after': wait_time},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            original_url = request.data.get('original_url')
            
            if not original_url:
                return Response(
                    {'error': 'original_url is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # check if url already exists
            existing_url = ShortURL.objects.filter(original_url=original_url).first()
            if existing_url:
                serializer = ShortURLSerializer(existing_url)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # generate short url
            shortened_url = generate_short_url(original_url)
            
            # save to db
            short_url_obj = ShortURL.objects.create(
                original_url=original_url,
                shortened_url=shortened_url
            )
            
            serializer = ShortURLSerializer(short_url_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response(
                {'error': 'Failed to create short URL'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RedirectShortURLView(APIView):
    def get(self, request, shortened_url):
        try:
            short_url_obj = ShortURL.objects.get(shortened_url=shortened_url)
            
            try:
                #create click
                Click.objects.create(url=short_url_obj)
            except Exception:
                #do nothing to ensure redirection even when click obj creation fails.
                pass
            
            #redirect to original
            return redirect(short_url_obj.original_url)
        except ShortURL.DoesNotExist:
            return Response(
                {'error': 'Short URL not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListShortURLsView(APIView):
    def get(self, request):
        try:
            urls = ShortURL.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = int(os.getenv('PAGE_SIZE'))
            paginated_urls = paginator.paginate_queryset(urls, request)
            serializer = ShortURLSerializer(paginated_urls, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClicksView(APIView):
    def get(self, request, shortened_url):
        try:
            data = get_clicks_for_url(shortened_url)
            
            serializer = ClickSerializer(data['clicks'], many=True)
            return Response({
                'shortened_url': shortened_url,
                'original_url': data['url_obj'].original_url,
                'total_clicks_7d': data['total_count'],
                'clicks': serializer.data
            }, status=status.HTTP_200_OK)
        except ShortURL.DoesNotExist:
            return Response(
                {'error': 'Short URL not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )