# Extracts a filtered .csv file from comments.json

import json
import pandas as pd
import os
import csv

input_path = 'data/comments.json'
output_path = 'data/filtered_comments.csv'

batch_size = 10000
batch = []
seen_ids = set()
skipped = 0
saved = 0

def should_use_text_field(comment):
    """
    Determines if the extracted text field should be used instead of the comment field.
    Extracted text exists when commenter has attached a file instead of writing a comment.
    """
    if comment is None:
        return True
    comment = comment.strip().lower()
    return (
        comment == '' or
        'attachment' in comment or
        'please see' in comment or
        'attached' in comment
    )

with open(input_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        try:
            item = json.loads(line)
            data = item.get('data', {})
            attributes = data.get('attributes', {})

            raw_comment = attributes.get('comment')
            extracted_text = item.get('text')

            if should_use_text_field(raw_comment) and extracted_text:
                final_comment = extracted_text
            else:
                final_comment = raw_comment

            if not final_comment:
                skipped += 1
                continue

            comment_id = data.get('id')
            if comment_id in seen_ids:
                skipped += 1
                continue
            seen_ids.add(comment_id)

            comment_data = {
                'comment': final_comment,
                'agency': attributes.get('agencyId'),
                'postedDate': attributes.get('postedDate'),
                'docketId': attributes.get('docketId'),
                'commentId': comment_id,
                'attachmentUrl': data.get('relationships', {}).get('attachments', {}).get('links', {}).get('related')
            }

            batch.append(comment_data)
            saved += 1

        except Exception as e:
            print(f"Skipping line {i} due to error: {e}")
            skipped += 1
            continue

        if len(batch) >= batch_size:
            pd.DataFrame(batch).to_csv(output_path, mode='a', index=False,
                                       header=not os.path.exists(output_path),
                                       quoting=csv.QUOTE_ALL)
            batch = []

if batch:
    pd.DataFrame(batch).to_csv(output_path, mode='a', index=False,
                               header=not os.path.exists(output_path),
                               quoting=csv.QUOTE_ALL)

print(f"\n✅ Done! Saved {saved} comments, skipped {skipped}.\n")