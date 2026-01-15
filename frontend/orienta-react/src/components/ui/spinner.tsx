import type { ComponentProps } from "react";
import { Loader2Icon } from "lucide-react";

import { cn } from "@/lib/utils";

type SpinnerProps = ComponentProps<typeof Loader2Icon>;

function Spinner({ className, ...props }: SpinnerProps) {
  return (
    <Loader2Icon
      role="status"
      aria-label="Loading"
      className={cn("size-4 animate-spin", className)}
      {...props}
    />
  );
}

export { Spinner };
