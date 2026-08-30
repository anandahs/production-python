from click.testing import CliRunner

from salesreport.cli import cli


def test_validate_reports_skipped_rows(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "store_id,quantity,unit_price\n"
        "S001,2,10.00\n"
        ",3,12.00\n"
        "S002,,5.00\n"
        "S003,abc,9.00\n"
        "S004,4,8.00\n"
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--input", str(csv_path)])

    assert result.exit_code == 0
    assert "Skipped 3 rows" in result.output
    assert "missing store_id" in result.output
    assert "missing quantity" in result.output
    assert "invalid quantity" in result.output
