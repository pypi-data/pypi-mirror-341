"""Assessment commands for the MontyCloud DAY2 CLI."""

import json

import click
from rich.console import Console
from rich.table import Table

from day2 import Session
from day2.exceptions import MontyCloudError
from day2.models.assessment import AnswerQuestionInput, CreateAssessmentInput
from day2_cli.utils.formatters import format_error

console = Console()


@click.group()
def assessment() -> None:
    """Assessment commands."""


@assessment.command("list")
@click.argument("tenant-id")
@click.option(
    "--status", type=str, required=True, help="Status filter (PENDING or COMPLETED)"
)
@click.option("--keyword", type=str, help="Keyword to filter by name or description")
@click.option("--page-number", type=int, default=1, help="Page number")
@click.option("--page-size", type=int, default=10, help="Page size")
def list_assessments(
    tenant_id: str, status: str, keyword: str, page_number: int, page_size: int
) -> None:
    """List assessments for a tenant.

    TENANT-ID: ID of the tenant to list assessments for.
    """
    try:
        session = Session()

        # Call the client method with explicit parameters
        result = session.assessment.list_assessments(
            tenant_id=tenant_id,
            status=status,
            keyword=keyword if keyword else None,
            page_number=page_number,
            page_size=page_size,
        )

        if not result.assessments:
            console.print("[yellow]No assessments found.[/yellow]")
            return

        table = Table(title=f"Assessments for Tenant: {tenant_id}")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="blue")
        table.add_column("Total Questions", style="magenta")
        table.add_column("Answered Questions", style="yellow")
        table.add_column("Created At", style="dim")

        for assessment_item in result.assessments:
            created_at = (
                assessment_item.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if assessment_item.created_at
                else "N/A"
            )
            table.add_row(
                assessment_item.id,
                assessment_item.name,
                assessment_item.status,
                str(assessment_item.total_questions),
                str(assessment_item.answered_questions),
                created_at,
            )

        console.print(table)

        # Display pagination information
        if result.has_more:
            console.print(
                f"[yellow]More results available. Current page: {result.page_number}[/yellow]"
            )
        else:
            console.print(f"[yellow]Current page: {result.page_number}[/yellow]")

    except MontyCloudError as e:
        console.print(format_error(e))


@assessment.command("get")
@click.argument("tenant-id")
@click.argument("assessment-id")
def get_assessment(tenant_id: str, assessment_id: str) -> None:
    """Get details of a specific assessment.

    TENANT-ID: ID of the tenant the assessment belongs to.
    ASSESSMENT-ID: ID of the assessment to get details for.
    """
    try:
        session = Session()
        result = session.assessment.get_assessment(tenant_id, assessment_id)

        table = Table(title=f"Assessment: {result.name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("ID", result.id)
        table.add_row("Name", result.name)
        table.add_row("Description", result.description or "N/A")
        table.add_row("Status", result.status)
        table.add_row("ARN", result.assessment_arn or "N/A")
        table.add_row("Owner", result.owner or "N/A")
        table.add_row("Lenses", ", ".join(result.lenses) if result.lenses else "N/A")
        table.add_row("Total Questions", str(result.total_questions))
        table.add_row("Answered Questions", str(result.answered_questions))
        table.add_row(
            "Created At",
            (
                result.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if result.created_at
                else "N/A"
            ),
        )
        table.add_row(
            "Updated At",
            (
                result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                if result.updated_at
                else "N/A"
            ),
        )

        console.print(table)

    except MontyCloudError as e:
        console.print(format_error(e))


@assessment.command("create")
@click.argument("tenant-id")
@click.option("--name", required=True, help="Assessment name")
@click.option("--description", required=True, help="Assessment description")
@click.option("--review-owner", required=True, help="Email of the review owner")
@click.option("--scope", required=True, help="JSON string representing the scope")
@click.option("--lenses", help="Comma-separated list of lenses")
def create_assessment(
    tenant_id: str,
    name: str,
    description: str,
    review_owner: str,
    scope: str,
    lenses: str,
) -> None:
    """Create a new assessment.

    TENANT-ID: ID of the tenant to create the assessment in.
    """
    try:
        session = Session()

        # Parse the scope JSON string
        try:
            scope_data = json.loads(scope)
            if not isinstance(scope_data, list):
                scope_data = [scope_data]
        except json.JSONDecodeError:
            console.print("[red]Error: Scope must be a valid JSON string[/red]")
            return

        # Parse lenses if provided
        lenses_list = []
        if lenses:
            lenses_list = [lens.strip() for lens in lenses.split(",")]

        # Create a proper CreateAssessmentInput object
        assessment_input = CreateAssessmentInput(
            AssessmentName=name,
            Description=description,
            ReviewOwner=review_owner,
            Scope=scope_data,
            Lenses=lenses_list,
        )

        result = session.assessment.create_assessment(
            tenant_id=tenant_id, data=assessment_input
        )

        console.print("[green]Assessment created successfully![/green]")
        console.print(f"Assessment ID: [cyan]{result.id}[/cyan]")
        console.print(f"Assessment Name: [green]{result.name}[/green]")

    except MontyCloudError as e:
        console.print(format_error(e))


@assessment.command("questions")
@click.argument("tenant-id")
@click.argument("assessment-id")
@click.argument("pillar-id")
def list_questions(tenant_id: str, assessment_id: str, pillar_id: str) -> None:
    """List questions for a specific pillar in an assessment.

    TENANT-ID: ID of the tenant the assessment belongs to.
    ASSESSMENT-ID: ID of the assessment to get questions for.
    PILLAR-ID: ID of the pillar to get questions for (e.g., operational-excellence, security).
    """
    try:
        session = Session()
        result = session.assessment.list_questions(tenant_id, assessment_id, pillar_id)

        # Display pillar information
        console.print(f"[bold]Pillar:[/bold] {pillar_id}")
        # Ensure we handle None values properly for the calculation
        total = result.total_questions or 0
        answered = result.answered_questions or 0
        remaining = total - answered

        console.print(
            f"[bold]Questions:[/bold] {total} total, "
            f"{answered} answered, "
            f"{remaining} remaining"
        )
        console.print("\n")

        # Create a table for the questions
        table = Table(title=f"Questions for Pillar: {pillar_id}")
        table.add_column("#", style="dim")
        table.add_column("Question ID", style="cyan")
        table.add_column("Title", style="green", width=40)
        table.add_column("Status", style="yellow")
        table.add_column("Risk", style="red")

        # Add rows for each question
        for i, question in enumerate(result.questions, 1):
            status = (
                "[green]Answered[/green]"
                if question.is_answered
                else "[yellow]Not Answered[/yellow]"
            )
            risk = question.risk if question.risk else "N/A"

            table.add_row(
                str(i),
                question.id,
                question.title,
                status,
                risk,
            )

        console.print(table)

        # If user wants to see more details about a specific question
        console.print(
            "\n[dim]To see details of a specific question, use the 'question get' command with the Question ID.[/dim]"
        )

    except MontyCloudError as e:
        console.print(format_error(e))


@assessment.command("question")
@click.argument("tenant-id")
@click.argument("assessment-id")
@click.argument("question-id")
def get_question(tenant_id: str, assessment_id: str, question_id: str) -> None:
    """Get details of a specific question in an assessment.

    TENANT-ID: ID of the tenant the assessment belongs to.
    ASSESSMENT-ID: ID of the assessment the question belongs to.
    QUESTION-ID: ID of the question to get details for.
    """
    try:
        session = Session()
        result = session.assessment.get_question(tenant_id, assessment_id, question_id)

        # Display question details
        console.print(f"[bold]Question:[/bold] {result.title}")
        console.print(f"[bold]ID:[/bold] {result.id}")
        console.print(f"[bold]Pillar:[/bold] {result.pillar_name} ({result.pillar_id})")
        console.print(f"[bold]Description:[/bold] {result.description}")

        # Show status and risk information
        status = (
            "[green]Answered[/green]"
            if result.is_answered
            else "[yellow]Not Answered[/yellow]"
        )
        console.print(f"[bold]Status:[/bold] {status}")

        if result.is_answered:
            console.print(f"[bold]Risk:[/bold] {result.risk or 'Not specified'}")
            console.print(f"[bold]Reason:[/bold] {result.reason or 'Not provided'}")
            if result.notes:
                console.print(f"[bold]Notes:[/bold] {result.notes}")

            if result.selected_choices or result.choice_answers:
                console.print("\n[bold]Selected Choices:[/bold]")
                # Use selected_choices or choice_answers, whichever is available
                choice_ids = result.selected_choices or result.choice_answers

                for choice_id in choice_ids:
                    # Handle both string and dictionary formats for choice_answers
                    if isinstance(choice_id, dict) and "ChoiceId" in choice_id:
                        choice_id = choice_id["ChoiceId"]

                    # Find the choice title if available
                    choice_title = next(
                        (
                            choice["Title"]
                            for choice in result.choices
                            if choice["ChoiceId"] == choice_id
                        ),
                        "Unknown",
                    )
                    console.print(f"  • {choice_title} ({choice_id})")

        # Display available choices
        if result.choices:
            console.print("\n[bold]Available Choices:[/bold]")
            for choice in result.choices:
                console.print(f"  • {choice['Title']} ({choice['ChoiceId']})")

        # Show hint for answering the question
        if not result.is_answered:
            console.print(
                "\n[dim]To answer this question, use the 'answer' command.[/dim]"
            )

    except MontyCloudError as e:
        console.print(format_error(e))


@assessment.command("answer")
@click.argument("tenant-id")
@click.argument("assessment-id")
@click.argument("question-id")
@click.option(
    "--reason",
    required=True,
    type=click.Choice(
        [
            "OUT_OF_SCOPE",
            "BUSINESS_PRIORITIES",
            "ARCHITECTURE_CONSTRAINTS",
            "OTHER",
            "NONE",
        ]
    ),
    help="Reason for the answer",
)
@click.option(
    "--choices", help="Comma-separated list of choice IDs to mark as selected"
)
@click.option("--notes", help="Additional notes about the answer")
@click.option(
    "--applicable/--not-applicable",
    default=True,
    help="Whether the question is applicable to the workload",
)
def answer_question(
    tenant_id: str,
    assessment_id: str,
    question_id: str,
    reason: str,
    choices: str,
    notes: str,
    applicable: bool,
) -> None:
    """Answer a specific question in an assessment.

    TENANT-ID: ID of the tenant the assessment belongs to.
    ASSESSMENT-ID: ID of the assessment the question belongs to.
    QUESTION-ID: ID of the question to answer.
    """
    try:
        session = Session()

        # Parse selected choices if provided and create choice_updates dictionary
        choice_updates = {}
        if choices:
            for choice_id in [choice.strip() for choice in choices.split(",")]:
                choice_updates[choice_id] = {"Status": "SELECTED"}

        # Create the answer input with the new format
        answer_data = AnswerQuestionInput(
            LensAlias="wellarchitected",
            ChoiceUpdates=choice_updates,
            Reason=reason,
            Notes=notes or "",
            IsApplicable=applicable,
        )

        # Submit the answer
        result = session.assessment.answer_question(
            tenant_id, assessment_id, question_id, answer_data
        )

        # Display result
        console.print(f"[green]{result.message}[/green]")
        console.print(f"[bold]Status:[/bold] {result.status}")
        console.print(f"[bold]Question ID:[/bold] {result.id}")

        # Show a summary of what was submitted
        console.print("\n[bold]Answer Summary:[/bold]")
        if choices:
            console.print(f"[bold]Selected Choices:[/bold] {choices}")
        console.print(f"[bold]Reason:[/bold] {reason}")
        if notes:
            console.print(f"[bold]Notes:[/bold] {notes}")
        if not applicable:
            console.print("[bold]Applicability:[/bold] Not applicable to this workload")

        console.print(
            "\n[dim]To view the updated question details, use the 'question' command.[/dim]"
        )

    except MontyCloudError as e:
        console.print(format_error(e))
