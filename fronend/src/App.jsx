import { Route, Routes  }  from "react-router-dom";
import {AuthPage} from "./pages/AuthPage";
import {Page404} from "./pages/Page404";
import {MainPage} from "./pages/MainPage";

export const App = () => {

  return (
      <Routes>
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/" element={<MainPage />} />
          <Route path="*" element={<Page404 />} />

      </Routes>
  );
};

