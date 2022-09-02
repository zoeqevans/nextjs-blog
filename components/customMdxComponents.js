import styles from "./layout.module.css";

const MdxAnchorElement = (props) => (
  <a href={props.href} className={styles.link}>
    {props.children}
  </a>
);

const customMdxComponents = {
  a: MdxAnchorElement,
};

export default customMdxComponents;
