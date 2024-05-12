import { ReactNode } from "react";
import { Button, Card, ListGroup, Spinner } from "react-bootstrap";
import { ArrowClockwise } from "react-bootstrap-icons";

type TCardListProps = {
  title?: string;
  refreshHandler?: () => void;
  isLoadingContent?: boolean;
  children: ReactNode;
};

export function CardList({
  title,
  refreshHandler,
  isLoadingContent,
  children,
}: TCardListProps): ReactNode {
  return (
    <Card className="m-2">
      {title && (
        <Card.Header className="justify-content-between d-flex">
          <Card.Text>{title?.toUpperCase()}</Card.Text>
          <Button
            onClick={() => refreshHandler?.()}
            variant="primary"
            disabled={isLoadingContent}
          >
            {isLoadingContent ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />
                <span className="visually-hidden">Loading...</span>
              </>
            ) : (
              <ArrowClockwise />
            )}
          </Button>
        </Card.Header>
      )}
      <ListGroup variant="flush">
        <ListGroup.Item>{children}</ListGroup.Item>
      </ListGroup>
    </Card>
  );
}
