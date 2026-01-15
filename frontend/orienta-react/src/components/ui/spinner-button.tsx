import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

type SpinnerButtonProps = ComponentProps<typeof Button>;

function SpinnerButton({ className, size, ...props }: SpinnerButtonProps) {
  return (
    <Button className={className} size={size} disabled {...props}>
      <Spinner />
      {props.children}
    </Button>
  );
}

export { SpinnerButton };
