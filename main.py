from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse

from database import get_connection, create_table
from schemas import TicketCreate, TicketResponse
from utils import calculate_response_deadline


app = FastAPI(
    title="Customer Support Ticket API",
    description="API for creating and managing customer support tickets"
)


create_table()


@app.get("/")
def home():
    return {"message": "Customer Support Ticket API is running"}


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):

    created_at = datetime.now()
    response_deadline = calculate_response_deadline(created_at)

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tickets
        (title, description, status, tags, created_at, response_deadline)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticket.title,
            ticket.description,
            ticket.status,
            ticket.tags,
            created_at.isoformat(),
            response_deadline.isoformat()
        )
    )

    connection.commit()

    ticket_id = cursor.lastrowid

    connection.close()

    return {
        "id": ticket_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "tags": ticket.tags,
        "created_at": created_at.isoformat(),
        "response_deadline": response_deadline.isoformat()
    }


@app.get("/tickets")
def get_tickets():

    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tickets"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):

    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return dict(row)


@app.post("/tickets/web-submit", response_class=HTMLResponse)
def web_submit(
    title: str = Form(...),
    description: str = Form(...),
    status: Literal["Open", "In Progress", "Closed"] = Form(...),
    tags: str = Form("")
):

    created_at = datetime.now()
    response_deadline = calculate_response_deadline(created_at)

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO tickets
        (title, description, status, tags, created_at, response_deadline)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            status,
            tags,
            created_at.isoformat(),
            response_deadline.isoformat()
        )
    )

    connection.commit()
    connection.close()

    return "<h1>Ticket Created Successfully!</h1>"