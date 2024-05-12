import { ReactNode } from "react";
import { Card, ListGroup, Placeholder } from "react-bootstrap";

type TCardListPlaceholderProps = {
  title?: string;
};

export function CardListPlaceholder({
  title,
}: TCardListPlaceholderProps): ReactNode {
  return (
    <Card className="m-2">
      {title && (
        <Card.Header className="justify-content-between d-flex">
          <Card.Text>{title?.toUpperCase()}</Card.Text>
        </Card.Header>
      )}
      <ListGroup variant="flush">
        <ListGroup.Item>
          <Placeholder as={Card.Title} animation="glow">
            <Placeholder xs={6} />
          </Placeholder>
          <Placeholder as={Card.Text} animation="glow">
            <Placeholder xs={4} /> <Placeholder xs={4} /> {"  "}
            <Placeholder xs={6} />
          </Placeholder>
        </ListGroup.Item>
        <ListGroup.Item>
          <Placeholder as={Card.Title} animation="glow">
            <Placeholder xs={6} />
          </Placeholder>
          <Placeholder as={Card.Text} animation="glow">
            <Placeholder xs={4} /> <Placeholder xs={4} /> {"  "}
            <Placeholder xs={6} />
          </Placeholder>
        </ListGroup.Item>
      </ListGroup>
    </Card>
  );
}
