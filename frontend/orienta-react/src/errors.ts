import { ErrorResponse } from "./schemas/errorSchema";

export class APIError extends Error {
  public readonly action!: string;
  public readonly code!: number;

  constructor(error: ErrorResponse) {
    super();
    Object.assign(this, error);
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      action: this.action,
      status_code: this.code,
    };
  }
}
