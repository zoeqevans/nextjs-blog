import styles from "./betting-charts.module.css";

export default function BettingCharts() {
  const ids_promo_false = [
    "291642c0-2099-4e98-9d68-551d8f8e98f2",
    "4dcaef48-dd6c-42e2-8bea-ea42b0e72e1e",
    "f019e916-1933-481e-bf89-828e60b65468",
  ];
  const ids_promo_true = [
    "e6405570-0d44-42dd-9322-0d0cf0b6cc1e",
    "cd9b00dd-9777-4d94-a797-c0271c4b950c",
    "b8644b67-740b-4f66-ab7f-8c5b990e9cbd",
  ];

  return (
    <div id="plotly-charts" className={styles.chartsContainer}>
      <div></div>
      <div className={styles.chartsTitle}>
        <p>How to Bet When...</p>

        <div className={styles.divider} />
      </div>
      <div></div>
      <div className={styles.colTitle}>
        Risk Aversion = 1 <br />
        (Losses And Gains Treated Equally)
      </div>
      <div className={styles.colTitle}>
        Risk Aversion = 2 <br />
        (Normal)
      </div>
      <div className={styles.colTitle}>
        Risk Aversion = 100 <br />
        (Any Loss is Unacceptable)
      </div>
      <div className={styles.rowLabel}>
        The Bet Token <strong>does not</strong> return its stake upon winning
      </div>
      {ids_promo_false.map((id) => (
        <div id={id} key={id} className="plotly-chart-div" />
      ))}
      <div className={styles.rowLabel}>
        The Bet Token <strong>does</strong> return its stake upon winning
      </div>
      {ids_promo_true.map((id) => (
        <div id={id} key={id} className="plotly-chart-div" />
      ))}
    </div>
  );
}
