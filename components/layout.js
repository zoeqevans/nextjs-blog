import Head from "next/head";
import Image from "next/image";
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

  const [personalDetails, setPersonalDetails] = useState();

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
  const twitterUrl = `https://twitter.com/${personalDetails?.twitter}`;
  const githubUrl = `https://github.com/${personalDetails?.github}`;

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
        <div className={styles.navDivider} />

        <div className={styles.navBar}>
          <Link href="/" className={styles.link}>
            <a>
              <span className={styles.span}>Posts</span>
            </a>
          </Link>
          <Link href="/about">
            <a>
              <span className={styles.span}>About</span>
            </a>
          </Link>

          <span className={styles.span}>
            <Link href={twitterUrl}>
              <a>
                <Image
                  src="/images/twitter.svg"
                  height="40px"
                  width="40px"
                ></Image>
              </a>
            </Link>
          </span>
          <span className={styles.span}>
            <Link href={githubUrl}>
              <a>
                <Image
                  src="/images/github.svg"
                  height="40px"
                  width="40px"
                ></Image>
              </a>
            </Link>
          </span>
        </div>
        <div className={styles.divider} />
      </header>
      <div className={styles.contentContainer}>
        <main>{children}</main>
      </div>
    </div>
  );
}
