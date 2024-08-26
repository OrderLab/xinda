set number
set ignorecase
set hlsearch
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if has("autocmd")
  " Make vim jump to the last position when reopening a file
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

  " Indentation based on filetype
  filetype plugin indent on
endif

" Enable spell-check
" set spell spelllang=en_us

" When split, split to the right
set splitright

" Highlight current line
set cursorline
hi cursorline term=underline cterm=underline ctermbg=NONE gui=underline

" Don't tab, space!
set tabstop=4
set shiftwidth=2
set expandtab

" Auto indentation
" set autoindent
"
" " Show (partial) command in status line
set showcmd

if has('cmdline_info')
  set ruler                   " Show the ruler
  set rulerformat=%30(%=\:b%n%y%m%r%w\ %l,%c%V\ %P%) " A ruler on steroids
  set showcmd                 " Show partial commands in status line and
endif

set laststatus=2
if has('statusline')
  set laststatus=2

  set statusline=%<%f\                     " Filename
  set statusline+=%w%h%m%r                 " Options
  set statusline+=\ [%{&ff}/%Y]            " Filetype
  set statusline+=\ [%{getcwd()}/%f]       " Current pwd
  set statusline+=%=%-14.(%l,%c%V%)\ %p%%  " Right aligned file nav info
endif


