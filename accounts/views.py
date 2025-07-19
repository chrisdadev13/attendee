from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from bots.models import Project


@login_required
def home(request):
    # Get the first bot for the user's organization
    project = Project.objects.filter(organization=request.user.organization).first()
    if not project:
        project = Project.objects.create(
            name=f"{request.user.email}'s project",
            organization=request.user.organization,
        )
    if project:
        return redirect("projects:project-dashboard", object_id=project.object_id)
    raise Http404("No projects found for this organization. You need to create a project first.")


def debug_session(request):
    """Temporary debug view to test session handling"""
    if request.user.is_authenticated:
        return HttpResponse(f"""
        <h1>Success! You are logged in as {request.user.email}</h1>
        <p>Session key: {request.session.session_key}</p>
        <p>User ID: {request.user.id}</p>
        <p><a href="/">Go to home</a></p>
        """)
    else:
        return HttpResponse("""
        <h1>Not authenticated</h1>
        <p>Session key: """ + str(request.session.session_key) + """</p>
        <p><a href="/accounts/login/">Login</a></p>
        """)
