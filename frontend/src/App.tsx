import { ReactNode, useEffect, useState } from "react";
import { Header } from "./components/Header";
import { config } from "./misc/config";
import { clearCookie, getCookie } from "./misc/cookies";
import { userLogin } from "./misc/userLogin";
import { Activities } from "./views/Activities";
import { TAthlete } from "./misc/types";
import { getAthlete } from "./misc/getAthlete";
import ErrorToast from "./components/ErrorToast";
import { Col, Container, Row } from "react-bootstrap";
import { refreshSession } from "./misc/refreshSession";

function App(): ReactNode {
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [sessionId, setSessionId] = useState<string>();
  const [athleteInfo, setAthleteInfo] = useState<TAthlete>();

  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingAthleteInfo, setIsLoadingAthleteInfo] = useState(false);

  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorToastReason, setErrorToastReason] = useState<Error>({
    name: "-",
    message: "-",
  });

  const loginHandler = () => {
    if (!sessionId) {
      loadSessionCookie();
      return;
    }
    if (!isSignedIn) {
      if (isLoading) return;

      console.debug("User Sign-In");
      const controller = new AbortController();
      setIsLoading(true);
      refreshSession(
        controller.signal,
        () => {
          setIsLoading(false);
          setIsSignedIn(true);
          loadSessionCookie();
        },
        (reason: Error) => {
          setIsLoading(false);
          setErrorToastReason(reason);
          setShowErrorToast(true);
          setIsSignedIn(false);
          clearCookie(config.SESSION_COOKIE_NAME);
        }
      );
      return;
    }
  };

  const loadSessionCookie = () => {
    console.debug("Loading session cookie..");
    const session = getCookie(config.SESSION_COOKIE_NAME);
    if (!session) {
      console.debug("No session cookie found.");
      userLogin();
      return;
    }
    console.debug("Loaded session cookie: " + session);
    setSessionId(session);
  };

  useEffect(() => {
    if (!sessionId) return;

    const loadAthleteInfo = () => {
      if (isLoadingAthleteInfo) return;
      const controller = new AbortController();
      setIsLoading(true);
      getAthlete(
        controller.signal,
        (info: TAthlete) => {
          setIsLoadingAthleteInfo(false);
          setAthleteInfo(info);
          setIsSignedIn(true);
        },
        (reason: Error) => {
          setIsLoadingAthleteInfo(false);
          setErrorToastReason(reason);
          setShowErrorToast(true);
          setIsSignedIn(false);
          clearCookie(config.SESSION_COOKIE_NAME);
        }
      );
    };

    loadAthleteInfo();
  }, [sessionId]);

  return (
    <>
      <ErrorToast
        show={showErrorToast}
        setShow={setShowErrorToast}
        reason={errorToastReason}
      />
      <Header
        loginHandler={loginHandler}
        isSignedIn={isSignedIn}
        athlete={athleteInfo}
      />
      <Container>
        <Row>
          <Col md>
            <Activities isSignedIn={isSignedIn} />
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default App;
