import time
import logging
from django.http import JsonResponse
from django.views import View
from .services.job_search_service import (
    LinkedinJobSearchServiceAutomation,
    DjangoJobsSearchAutomation,
)

logger = logging.getLogger(__name__)


class LinkedinJobSearchView(View):

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""
        email = request.GET.get("email")
        password = request.GET.get("password")
        keyword = request.GET.get("keyword")

        try:
            # Instantiate the service with the necessary parameters
            job_search_service = LinkedinJobSearchServiceAutomation(
                email=email, password=password, keyword=keyword
            )
            job_search_service.apply_to_jobs()
            time.sleep(10)

            # Return the applications collected
            return JsonResponse(
                {"status": "success", "applications": job_search_service.applications}
            )
        except Exception as e:
            logger.error(f"Error during job application process: {e}")
            input("PRES ANY BUTTON TO CLOSE THE DRIVER...")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


class DjangoJobsSearchView(View):

    def get(self, request, *args, **kwargs):
        job_search_service = DjangoJobsSearchAutomation()
        job_search_service.scrape_djangojobs()
        return JsonResponse({"status": "success"})
