import styles from "../styles/global.css";

import { MDXProvider } from "@mdx-js/react";
import customMdxComponents from "../components/customMdxComponents";
//import ReactGA from "react-ga";

import { GoogleAnalytics } from "nextjs-google-analytics";

export default function App({ Component, pageProps }) {
  return (
    <>
      <GoogleAnalytics trackPageViews gaMeasurementId="G-X7P2QW3WPH" />
      <MDXProvider components={customMdxComponents}>
        <Component {...pageProps} />
      </MDXProvider>
    </>
  );
}
