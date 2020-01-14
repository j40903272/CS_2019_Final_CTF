#include <stdio.h>
#include <time.h>
#include <stdlib.h>

// #define __ROL__(x, y) _rotl(x, y)
// inline unsigned int __ROL4__(unsigned int value, int count) { return __ROL__((unsigned int)value, count); }
// inline unsigned int __ROR4__(unsigned int value, int count) { return __ROL__((unsigned int)value, -count); }

// int reverse(int inp, int r){
//     r = r%4;
//     if(r == 0)
//         return inp ^ 0xFACEB00C;
//     else if (r == 1)
//         return inp - 74628;
//     else if (r == 2)
//         return (__ROR4__(inp & 0xAAAAAAAA, 2) | __ROL4__(inp & 0x55555555, 4));
//     else if (r==3){
//         inp = (__ROR4__(inp & 0xAAAAAAAA, 2) | __ROL4__(inp & 0x55555555, 4));
//         inp = inp - 74628;
//         return inp ^ 0xFACEB00C;
//     }
// }

int main(){
    time_t Github = 1568179514;
//     // check if match
//     struct tm *v0;
//     v0 = gmtime(&Github);
//     printf("%d %02d %02d %02d %02d %02d\n", 
//     (unsigned int)(v0->tm_year + 1900),
//     (unsigned int)v0->tm_mon,
//     (unsigned int)v0->tm_wday,
//     (unsigned int)v0->tm_hour,
//     (unsigned int)v0->tm_min,(int)v0->tm_sec);
    srand(Github);
    int v2;
    for(int i = 0 ; i < 937436+1 ; i++){
        v2 = rand();
        printf("%d\n", v2);
    }
    
//     FILE* fin = fopen( "output.txt","rb" );
//     FILE* fout = fopen( "output.png","wb" );
//     char buffer[20];
//     int v2, x;
    
//     for(int i = 0 ; i < 937422 ; i++){
//         v2 = rand();
//         fread(buffer, sizeof(char), 4, fin);
//         x = atoi(buffer);
//         x = reverse(x, v2);
//         fprintf(fout, "%d", x);
//     }
    
//     fclose(fin);
//     fclose(fout);
}

