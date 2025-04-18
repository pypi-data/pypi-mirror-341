"""
Module: keywords
Provides functionality to extract keywords from subdomain lists.
"""
class SimpleGet:
    @staticmethod
    def get_keywords(args) -> list:
        """
        Generate a list of keywords by splitting on dots and hyphens from the provided subdomains list.
        """
        all_keywords = []
        with open(args.list, 'r') as file:
            for line in file:
                line = line.rstrip()
                # split on dots
                local_keywords = line.split('.')
                # also split on hyphens
                for keyword in list(local_keywords):
                    if '-' in keyword:
                        hyphen_keywords = keyword.split('-')
                        local_keywords.extend(hyphen_keywords)
                all_keywords.extend(local_keywords)
        # dedupe and return
        return list(set(all_keywords))