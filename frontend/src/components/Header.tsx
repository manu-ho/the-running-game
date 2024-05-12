import { ReactNode } from "react";
import { Image, Container, Navbar, NavbarText } from "react-bootstrap";
import { PersonCircle } from "react-bootstrap-icons";
import { TAthlete } from "../misc/types";

type THeaderProps = {
  loginHandler: () => void;
  isSignedIn: boolean;
  athlete?: TAthlete;
};

export function Header({
  loginHandler,
  isSignedIn,
  athlete,
}: THeaderProps): ReactNode {
  const handleUserProfileButtonClick = () => {
    if (isSignedIn) {
      console.debug("Already signed in!");
    } else {
      loginHandler();
    }
  };
  return (
    <Navbar bg="dark" data-bs-theme="dark" fixed="top">
      <Container fluid>
        <Navbar.Brand href="/">The Running Game 🏃🕹️</Navbar.Brand>
        <Navbar.Text>presented by Invalidentreff ☕🍰</Navbar.Text>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <div onClick={() => handleUserProfileButtonClick()}>
            <Navbar.Brand>{isSignedIn && athlete?.username}</Navbar.Brand>
            {isSignedIn ? (
              <Image
                src={athlete?.profile || athlete?.profile_medium}
                width="45"
                height="45"
                roundedCircle
              />
            ) : (
              <>
                <Navbar.Brand>Login</Navbar.Brand>
                <PersonCircle color="lightgrey" size="2em" />
              </>
            )}
          </div>
          <NavbarText></NavbarText>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
