import styles from "./layout.module.css";
import Image from "next/image";

const MdxAnchorElement = (props) => {
  const target = props.href[0] === "#" || props.href[0] === "/" ? "" : "_blank";
  return (
    <a target={target} href={props.href} className={styles.link}>
      {props.children}
    </a>
  );
};

const customMdxComponents = {
  a: MdxAnchorElement,
  // img: (props) => <Image layout="fill" {...props} />,
};

export default customMdxComponents;
