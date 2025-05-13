import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


DATE_PATTERN = re.compile(
    r"\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
)


def scrape_s2s_archive():
    BASE_URL = "https://cw3e.ucsd.edu/cw3e_s_and_s_outlook_archive/"
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch archive page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    dates = []

    table_rows = soup.select("table tr")
    for row in table_rows:
        tds = row.find_all("td")
        if len(tds) >= 2:
            p_tag = tds[1].find("p")
            if p_tag:
                match = DATE_PATTERN.search(p_tag.get_text())
                if match:
                    try:
                        parsed_date = datetime.strptime(match.group(), "%d %B %Y")
                        dates.append(parsed_date)
                    except ValueError:
                        continue
    return dates


def scrape_s2s_slides(date):
    prefixes = ["Subseasonal_Outlook", "S2S_Outlook", "Seasonal_Outlook"]
    folder_patterns = [f"{prefix}_%d%b%Y" for prefix in prefixes] + [
        f"{prefix}_%-d%b%Y" for prefix in prefixes
    ]
    extensions = [".png", ".PNG"]

    month_num = date.strftime("%m")
    year = date.strftime("%Y")
    date_str = date.strftime("%B %d, %Y")
    slide_numbers = []

    for pattern in folder_patterns:
        try:
            folder_name = date.strftime(pattern)
        except ValueError:
            # Handle platforms that don't support %-d (Windows)
            folder_name = date.strftime(
                pattern.replace("%-d", str(int(date.strftime("%d"))))
            )

        slide_number = 2
        found_any = False

        while True:
            success = False
            for ext in extensions:
                url = f"https://cw3e.ucsd.edu/wp-content/uploads/{year}/{month_num}/{folder_name}/Slide{slide_number}{ext}"
                response = requests.get(url)
                if response.status_code == 200:
                    slide_numbers.append(slide_number)
                    slide_number += 1
                    success = True
                    found_any = True
                    break  # stop checking other extensions for this slide

            if not success:
                break  # no extension worked, stop checking this slide number

        if found_any:
            return (date_str, slide_numbers)

    # If no folder patterns worked
    return (date_str, [])


def get_s2s_outlooks():
    dates = scrape_s2s_archive()
    # fmt: off
    slide_dict = {
        "January 21, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "February 25, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "February 11, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "February 18, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "January 28, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "March 18, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "March 11, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "February 04, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "March 04, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "November 18, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "January 14, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "December 20, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "November 26, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "December 10, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "November 19, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "January 07, 2025": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        "November 12, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        "December 03, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "November 06, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "March 22, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "March 15, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "March 07, 2024": [2, 3, 4, 5, 6, 7, 8, 9],
        "February 09, 2024": [2, 3, 4, 5, 6, 7, 8, 9],
        "March 08, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "February 16, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "March 01, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "January 31, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "February 23, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "February 02, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "January 17, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "January 26, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "December 11, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10],
        "January 03, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "January 09, 2024": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "December 20, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "December 13, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "March 17, 2023": [2],
        "January 27, 2023": [2],
        "February 03, 2023": [2],
        "November 17, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "January 06, 2023": [2],
        "December 01, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "April 03, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "January 13, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "November 03, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "February 13, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        "March 29, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "March 03, 2023": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "March 23, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "March 16, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "November 14, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "December 16, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "March 02, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "February 16, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "March 09, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "February 23, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "January 25, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "December 02, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        "January 12, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "December 22, 2021": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "February 09, 2022": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "December 08, 2021": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    }
    # fmt: on
    new_dates = [d for d in dates if d.strftime("%B %d, %Y") not in slide_dict]

    print(f"\nScraping slides in parallel for {len(new_dates)} new dates...\n")
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_date = {
            executor.submit(scrape_s2s_slides, date): date for date in new_dates
        }

        for future in as_completed(future_to_date):
            date_str, slide_numbers = future.result()
            slide_dict[date_str] = slide_numbers

    slide_dict = dict(
        sorted(
            slide_dict.items(),
            key=lambda item: datetime.strptime(item[0], "%B %d, %Y"),
            reverse=True,
        )
    )
    return slide_dict


if __name__ == "__main__":
    result = get_s2s_outlooks()
    print(result)
