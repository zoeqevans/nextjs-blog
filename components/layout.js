import Head from "next/head";
import Script from "next/script";
import styles from "./layout.module.css";
import utilStyles from "../styles/utils.module.css";
import Link from "next/link";

import { useState, useEffect } from "react";

export const usePersonalDetails = () => {
  const montyDetails = {
    fullName: "Monty Evans",
    email: "montyevans",
    twitter: "montymevans",
    github: "montyevans",
    monarch: "king",
  };

  const zoeDetails = {
    fullName: "Zoe Evans",
    email: "zoeqevans",
    twitter: "zoeqevans",
    github: "zoeqevans",
    monarch: "queen",
  };

  const [personalDetails, setPersonalDetails] = useState({ fullName: "|" });

  useEffect(() => {
    if (window.location.href.includes("zoeqevans.com")) {
      setPersonalDetails(zoeDetails);
    } else {
      setPersonalDetails(montyDetails);
    }
  }, []);

  return personalDetails;
};

export default function Layout({ children, meta }) {
  const personalDetails = usePersonalDetails();
  const fullName = personalDetails?.fullName;

  return (
    <div>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <title>{fullName}</title>
      </Head>

      <header className={styles.header}>
        <Link href="/" className={styles.link}>
          <a>
            <div className={styles.myName}>{fullName}</div>
          </a>
        </Link>

        <div className={styles.subtitle}>
          <em>Move Fast and Bake Things</em>
        </div>
        <div className={styles.divider} />
      </header>
      <div className={styles.contentContainer}>
        <main>{children}</main>
      </div>
    </div>
  );
}
