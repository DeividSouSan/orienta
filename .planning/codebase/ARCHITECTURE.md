# Architecture

## Overview
The project follows a decoupled layered architecture on the backend and a component-based architecture on the frontend.

## Backend Layers
1. **API Layer (`api/v1/`):** Flask Blueprints handling HTTP requests, using DTOs for input validation.
2. **DTO Layer (`dtos/`):** Pydantic models for data transfer between API and internal layers.
3. **Model/Service Layer (`models/`):** Domain logic, orchestration of data access, and integration with external services (Gemini, Firebase).
4. **Value Objects (`objects/`):** Domain-driven design (DDD) value objects for validating business rules (Email, Password).

## Frontend Architecture
- **Vite/React:** Component-based UI.
- **Client-Side Rendering:** Interaction with the Flask API.
- **TailwindCSS:** Utility-first styling.

## Data Flow
`User Request` -> `API Blueprint` -> `DTO Validation` -> `Model Logic` -> `External Service (Firebase/Gemini)` -> `Response`
