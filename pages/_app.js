import styles from "../styles/global.css";

import { MDXProvider } from "@mdx-js/react";

import customMdxComponents from "../components/customMdxComponents";

export default function App({ Component, pageProps }) {
  return (
    <MDXProvider components={customMdxComponents}>
      <Component {...pageProps} />
    </MDXProvider>
  );
}
