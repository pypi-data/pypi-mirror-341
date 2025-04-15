from typing import Optional
from num2words import num2words

def amount_in_words(
        amount: float,
        currency: str,
        lang: str,
        rem_fraction: bool = False,
        rounding: bool = False,
        title_style: bool = False,
        cap_style: bool = False,
        prefix_val: Optional[str] = None,
        subfix_val: Optional[str] = None,
        int_sep: Optional[str] = None,
        decimal_sep: Optional[str] = None) -> str:
    """
    Converts numerical amount to words with support for Indian and Bangladeshi currency formats.

    This function converts numerical amounts to words, with special handling for Indian Rupees (INR) 
    and Bangladeshi Taka (BDT). It supports various formatting options including rounding, fraction handling,
    and text styling.

        Args:
            amount (float): The numerical amount to convert to words.
            currency (str): Currency code ('INR', 'BDT', or other standard currency codes).
            lang (str): Language code for conversion (e.g., 'en', 'bn').
            rem_fraction (bool, optional): Whether to remove fractional parts. Defaults to False.
            rounding (bool, optional): Whether to round the amount. Takes precedence over rem_fraction. Defaults to False.
            title_style (bool, optional): Whether to apply title case to output. Defaults to False.
            cap_style (bool, optional): Whether to capitalize first letter only. Defaults to False.
            prefix_val (str, optional): Text to add before the amount words. Defaults to None.
            subfix_val (str, optional): Text to add after the amount words. Defaults to None.
            int_sep (str, optional): Separator for integer parts (e.g., 'and', ','). Defaults to None.
            decimal_sep (str, optional): Separator for decimal parts. Defaults to None.

        Returns:
            str: The amount converted to words with applied formatting.

        Examples:
            >>> amount_in_words(1234.56, 'INR', 'en')
            'One Thousand Two Hundred Thirty Four Rupees Fifty Six Paisa'
            
            >>> amount_in_words(5000, 'BDT', 'en', rounding=True)
            'Five Thousand Taka'
            
        **[rounding and rem_fraction]** ---> can't be both true at the same time.If This happens then
        **rounding** will be used.
        So, be careful about that and if you donot use rounding or rem_fraction the fuction will treat them as False by Default.
    """
    
    am2w=round_fraction_check(amount,rounding,rem_fraction,lang,currency,decimal_sep,int_sep)

    return text_styling(am2w,title_style,cap_style,prefix_val,subfix_val)
    
def round_fraction_check(amount: float,rounding: bool,rem_fraction:bool,lang: str,currency:str,decimal_sep:str,int_sep:str)->str:
    """Processes amount based on rounding and fraction preferences.

    Handles the core conversion logic with special processing for INR and BDT currencies,
    including proper handling of currency terms (rupee/taka and paisa).

    Args:
        amount (float): Numerical amount to process.
        rounding (bool): Whether to round the amount.
        rem_fraction (bool): Whether to remove fractional parts.
        lang (str): Language code for conversion.
        currency (str): Currency code.
        decimal_sep (str): Decimal separator character.
        int_sep (str): Integer part separator character.

    Returns:
        str: Processed amount in words with appropriate currency terms.
    """
    # Round, Fraction Checking
    eu = 'euro'
    dlr = 'dollar'
    ces = 'cents'
    ce = 'cent'
    bdt = "taka"
    inr="rupee"
    paisa = 'paisa'
    if (currency in ["BDT","INR"]):
        if rounding==True and rem_fraction==False:
            amount=round(amount)
            amount=float(amount)
            amount2w = (num2words(amount, to='currency', lang=lang)).lower()
            words = amount2w.split()
            amount2w = ' '.join(words[:-2])
            if amount2w.endswith(','):
                amount2w = amount2w[:-1]
                if not int_sep==None:
                    if int_sep==',':
                        amount2w=amount2w.replace("and",f" {int_sep}")
                    else:
                        amount2w=amount2w.replace(",",f" {int_sep}")
                else:
                    amount2w=amount2w
                
            else:
                amount2w=amount2w
                amount2w = int_separator(amount2w,int_sep)

        elif rounding==False and rem_fraction==True:
            amount2w = (num2words(amount, to='currency', lang=lang)).lower()
            words = amount2w.split()
            amount2w = ' '.join(words[:-3])
            if amount2w.endswith(','):
                amount2w = amount2w[:-1]
                if not int_sep==None:
                    if int_sep==',':
                        amount2w=amount2w.replace("and",f" {int_sep}")
                    else:
                        amount2w=amount2w.replace(",",f" {int_sep}")
                else:
                    amount2w=amount2w
            else:
                amount2w=amount2w
                amount2w = int_separator(amount2w,int_sep)
            
        elif rounding==True and rem_fraction==True:
            amount2w = (num2words(amount, to='currency', lang=lang)).lower()
            # amount2w=decimal_separator(amount2w,decimal_sep)
            amount2w = int_separator(amount2w,int_sep)
            
        else:
            amount2w = (num2words(amount, to='currency', lang=lang)).lower()
            # amount2w = decimal_separator(amount2w,decimal_sep)
            amount2w = int_separator(amount2w,int_sep)

        if (eu in amount2w) and (ce or ces in amount2w):
            if currency == "INR":
                am2w = amount2w.replace(eu, inr)
            else:
                am2w = amount2w.replace(eu, bdt)

            am2w = am2w.replace(ce, paisa)
            am2w = am2w.replace(ces, paisa)
        return am2w
    else:
        if rounding==True and rem_fraction==False:
            amount=round(amount)
            amount=float(amount)
            amount2w = (num2words(amount, to='currency',currency=currency,lang=lang)).lower()
            words = amount2w.split()
            amount2w = ' '.join(words[:-2])
            if amount2w.endswith(','):
                amount2w = amount2w[:-1]
                if not int_sep==None:
                    if int_sep==',':
                        amount2w=amount2w.replace("and",f" {int_sep}")
                    else:
                        amount2w=amount2w.replace(",",f" {int_sep}")
                else:
                    amount2w=amount2w
            else:
                amount2w=amount2w

        elif rounding==False and rem_fraction==True:
            amount2w = (num2words(amount, to='currency',currency=currency, lang=lang)).lower()
            words = amount2w.split()
            # print(f"After Split for rem fraction-------------->{words}")
            #change here to remove something if fraction removing gets any extra value
            amount2w = ' '.join(words[:-3])
            # print(f"After joining for rem fraction-------------->{amount2w}")
            if amount2w.endswith(','):
                amount2w = amount2w[:-1]
                if not int_sep==None:
                    if int_sep==',':
                        amount2w=amount2w.replace("and",f" {int_sep}")
                    else:
                        amount2w=amount2w.replace(",",f" {int_sep}")
                else:
                    amount2w=amount2w
            else:
                amount2w=amount2w

        elif rounding==True and rem_fraction==True:
            amount2w = (num2words(amount, to='currency',currency=currency, lang=lang)).lower()
            # amount2w=decimal_separator(amount2w,decimal_sep)
            amount2w = int_separator(amount2w,int_sep)
            
        else:
            amount2w = (num2words(amount, to='currency',currency=currency, lang=lang)).lower()
            # amount2w=decimal_separator(amount2w,decimal_sep)
            amount2w = int_separator(amount2w,int_sep)

        return amount2w

# def decimal_separator(amount2w,decimal_sep):
#     if decimal_sep!=None:
#         words = amount2w.split()
#         splited_amount2w = ' '.join(words[:-2])
#         if splited_amount2w.endswith(','):
#             amount2w_wc = amount2w[:-1]
#             amount2w = amount2w_wc+ f" {decimal_sep} {words[:-2]}"
#         else:
#             amount2w=amount2w
#     return amount2w

def int_separator(amount2w: str,int_sep: bool)->str:
    """Applies separator for integer parts of the amount.

    Handles the insertion of custom separators between integer parts of the amount,
    typically used for words like 'and' or comma.

    Args:
        amount2w (str): Amount in words to process.
        int_sep (str): Separator to insert between integer parts.

    Returns:
        str: Amount in words with applied integer separator.
    """
    words = amount2w.split()
    splited_amount2w = ' '.join(words[:-2])
    if splited_amount2w.endswith(','):
        if not int_sep==None:
            if int_sep==',':
                amount2w=amount2w.replace("and",f" {int_sep}")
            else:
                amount2w=amount2w.replace(",",f" {int_sep}")
        else:
            amount2w=amount2w
    return amount2w

#Text Styling
def text_styling(am2w: str,title_style: bool,cap_style: bool,prefix_val: Optional[str] = None,subfix_val: Optional[str] = None)->str:
    """Applies text styling to the converted amount.

    Handles various text formatting options including title case, capitalization,
    and addition of prefix/suffix values.

    Args:
        am2w (str): Amount in words to style.
        title_style (bool): Whether to apply title case.
        cap_style (bool): Whether to capitalize first letter only.
        prefix_val (str): Text to add before the amount.
        subfix_val (str): Text to add after the amount.

    Returns:
        str: Styled amount in words with any prefix/suffix additions.
    """
    if title_style==True:
        am2w=am2w.title()
        if not prefix_val==None:
            am2w=f"{prefix_val} {am2w}"
        else:
            am2w=am2w

        if not subfix_val==None:
            am2w=f"{am2w} {subfix_val} "
        else:
            am2w=am2w

        return am2w
    elif cap_style==True:
        am2w=am2w.capitalize()
        if not prefix_val==None:
            am2w=f"{prefix_val} {am2w}"
        else:
            am2w=am2w

        if not subfix_val==None:
            am2w=f"{am2w} {subfix_val} "
        else:
            am2w=am2w
        return am2w
    else:
        am2w=am2w.title()
        if not prefix_val==None:
            am2w=f"{prefix_val} {am2w}"
        else:
            am2w=am2w

        if not subfix_val==None:
            am2w=f"{am2w} {subfix_val} "
        else:
            am2w=am2w

        return am2w

if __name__ == "__main__":
    #Testing
    amount = float(input("Enter amount: "))
    currency = input("Enter currency (INR/BDT/USD/EUR/GBP): ")
    lang = input("Enter language (en_IN/bn): ")

    #string input to boolean conversion
    rem_fraction = input("Remove fraction? (y/n): ").lower() == 'y'
    rounding = input("Apply rounding? (y/n): ").lower() == 'y'
    title_style = input("Apply title style? (y/n): ").lower() == 'y'
    cap_style = input("Apply cap style? (y/n): ").lower() == 'y'
    
    #optional input vals
    prefix_val = input("Enter prefix (press Enter to skip): ") or None
    subfix_val = input("Enter subfix (press Enter to skip): ") or None
    int_sep = input("Enter integer separator (press Enter to skip): ") or None
    decimal_sep = input("Enter decimal separator (press Enter to skip): ") or None
    
    result = amount_in_words(
        amount=amount,
        currency=currency,
        lang=lang,
        rem_fraction=rem_fraction,
        rounding=rounding,
        title_style=title_style,
        cap_style=cap_style,
        prefix_val=prefix_val,
        subfix_val=subfix_val,
        int_sep=int_sep,
        decimal_sep=decimal_sep
    )
    print("\nAmount In Word:", result)