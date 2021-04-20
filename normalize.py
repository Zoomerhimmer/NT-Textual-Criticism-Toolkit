import re
import sys
import os

# Lists of same characters
alpha_equiv = ['Α','Ά','ά','ὰ','ά','ἀ','ἁ','ἂ','ἃ','ἄ','ἅ','ἆ','ἇ','Ἀ','Ἁ','Ἂ','Ἃ','Ἄ','Ἅ','Ἆ','Ἇ','ᾶ','Ᾰ','Ᾱ','Ὰ','Ά','ᾰ','ᾱ'] #Converts to α
alpha_subscripted = ['ᾀ','ᾁ','ᾂ','ᾃ','ᾄ','ᾅ','ᾆ','ᾇ','ᾈ','ᾉ','ᾊ','ᾋ','ᾌ','ᾍ','ᾎ','ᾏ','ᾲ','ᾴ','ᾷ','ᾼ','ᾳ'] #Converts to ᾳ
epsilon_equiv = ['Ε','Έ','έ','ὲ','έ','ἐ','ἑ','ἒ','ἓ','ἔ','ἕ','Ἐ','Ἑ','Ἒ','Ἓ','Ἔ','Ἕ'] #Converts to ε
eta_equiv = ['Η','Ή','ή','ὴ','ή','ἠ','ἡ','ἢ','ἣ','ἤ','ἥ','ἦ','ἧ','Ἠ','Ἡ','Ἢ','Ἣ','Ἤ','Ἥ','Ἦ','Ἧ','Ὲ','Έ','Ὴ','Ή','ῆ'] #Converts to η
eta_subscripted = ['ᾐ','ᾑ','ᾒ','ᾓ','ᾔ','ᾕ','ᾖ','ᾗ','ᾘ','ᾙ','ᾚ','ᾛ','ᾜ','ᾝ','ᾞ''ᾟ','ῂ','ῄ','ῇ','ῌ','ῃ'] #Converts to ῃ
iota_equiv = ['Ι','Ί','ΐ','Ϊ','ί','ϊ','ὶ','ί','ἰ','ἱ','ἲ','ἳ','ἴ','ἵ','ἶ','ἷ','Ἰ','Ἱ','Ἲ','Ἳ','Ἴ','Ἵ','Ἶ','Ἷ','ῐ','ῑ','ῒ','ΐ','ῖ','ῗ','Ῐ','Ῑ','Ὶ','Ί'] #Converts to ι
omicron_equiv = ['Ο','Ό','ό','ὸ','ό','ὀ','ὁ','ὂ','ὃ','ὄ','ὅ','Ὀ','Ὁ','Ὂ','Ὃ','Ὄ','Ὅ'] #Converts to ο
upsilon_equiv = ['Υ','Ύ','Ϋ','ΰ','ϋ','ύ','ὺ','ύ','ὐ','ὑ','ὒ','ὓ','ὔ','ὕ','ὖ','ὗ','Ὑ','Ὓ','Ὕ','Ὗ','ΰ','ῦ','ῧ','Ῠ','Ῡ','Ὺ','Ύ'] #Converts to υ
omega_equiv = ['Ω','Ώ','ώ','ὼ','ώ','ὠ','ὡ','ὢ','ὣ','ὤ','ὥ','ὦ','ὧ','Ὠ','Ὡ','Ὢ','Ὣ','Ὤ','Ὥ','Ὦ','Ὧ','ῶ','Ὸ','Ό','Ὼ','Ώ'] #Converts to ω
omega_subscripted = ['ᾠ','ᾡ','ᾢ','ᾣ','ᾤ','ᾥ','ᾦ','ᾧ','ᾨ','ᾩ','ᾪ','ᾫ','ᾬ','ᾭ','ᾮ','ᾯ','ῲ','ῴ','ῷ','ῼ','ῳ'] #Converts to ῳ
rho_equiv = ['Ρ','ῤ','ῥ','Ῥ'] #Converts to ρ
uppercase = {'Β':'β','Γ':'γ','Δ':'δ','Ζ':'ζ','Θ':'θ','Κ':'κ','Λ':'λ','Μ':'μ','Ν':'ν','Ξ':'ξ','Π':'π','Σ':'σ','Τ':'τ','Φ':'φ','Χ':'χ','Ψ':'ψ'}

def normalizer(char_list, normal_char, string):
    for char in char_list:
        string = string.replace(char, normal_char)
    return string

def normalize(data, ignore_subscript=True):
    # Remove brackets and normalize characters to textually significant letters
    data = re.sub(r'(\[|\])', '', data)
    data = normalizer(alpha_equiv, 'α', data)
    data = normalizer(epsilon_equiv, 'ε', data)
    data = normalizer(eta_equiv, 'η', data)
    data = normalizer(iota_equiv, 'ι', data)
    data = normalizer(omicron_equiv, 'ο', data)
    data = normalizer(upsilon_equiv, 'υ', data)
    data = normalizer(omega_equiv, 'ω', data)
    data = normalizer(rho_equiv, 'ρ', data)
    if ignore_subscript:
        data = normalizer(alpha_subscripted, 'α', data)
        data = normalizer(eta_subscripted, 'η', data)
        data = normalizer(omega_subscripted, 'ω', data)
    else:
        data = normalizer(alpha_subscripted, 'ᾳ', data)
        data = normalizer(eta_subscripted, 'ῃ', data)
        data = normalizer(omega_subscripted, 'ῳ', data)
    # Lowercase everything
    for cap in list(uppercase):
        data = data.replace(cap, uppercase[cap])
    return data

def main():
    # Prior checks
    arg_num = len(sys.argv)
    if  arg_num == 1:
        sys.exit('Program needs a file to process.')

    # Ignore iota subscripts by default
    try:
        if sys.argv[2].lower() == 'false':
            ignore_subscript = False
        else:
            ignore_subscript = True
    except:
        ignore_subscript = True
        print('Ignoring iota subscripts.')

    # Open files
    input = open(sys.argv[1])
    data = input.read()
    filename = os.path.splitext(sys.argv[1])[0] + '_normalized.txt'
    output = open(filename, 'w')

    data = normalize(data, ignore_subscript)
    output.write(data)

    # Close files
    input.close()
    output.close()

if __name__ == '__main__':
    main()
