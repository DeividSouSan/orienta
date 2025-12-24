import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

function SpinnerButton({ className, size, ...props }) {
    return (
        <Button className={className} size={size} disabled {...props}>
            <Spinner />
            {props.children}
        </Button>
    );
}

export {
    SpinnerButton
}
